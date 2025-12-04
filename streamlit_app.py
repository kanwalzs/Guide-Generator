import streamlit as st
import os, io, re, tempfile, zipfile, requests
from datetime import datetime
from urllib.parse import urlparse

# Reference: Language and Category Tags
# https://www.snowflake.com/en/developers/guides/get-started-with-guides/#language-and-category-tags

ALLOWED_LANGS = ["en","es","it","fr","de","ja","ko","pt_br"]
CATEGORIES_SOURCE_URL = "https://www.snowflake.com/en/developers/guides/get-started-with-guides/#language-and-category-tags"

# Fallback: minimal map in case live fetch/parse fails
CATEGORIES_FALLBACK = {
    "Quickstart": "snowflake-site:taxonomy/solution-center/certification/quickstart",
    "Snowflake Cortex": "snowflake-site:taxonomy/products/snowflake-cortex",
    "Snowpark": "snowflake-site:taxonomy/products/snowpark",
    "Streamlit In Snowflake": "snowflake-site:taxonomy/products/streamlit-in-snowflake",
    "Iceberg Tables": "snowflake-site:taxonomy/products/iceberg-tables",
    "Snowpipe Streaming": "snowflake-site:taxonomy/products/snowpipe-streaming",
    "Native Apps": "snowflake-site:taxonomy/products/native-apps",
    "External Tables": "snowflake-site:taxonomy/products/external-tables",
    "External Functions": "snowflake-site:taxonomy/products/external-functions",
    "Materialized Views": "snowflake-site:taxonomy/products/materialized-views",
    "Vector Data Type": "snowflake-site:taxonomy/products/vector-data-type",
    "Query Acceleration": "snowflake-site:taxonomy/products/query-acceleration",
    "Search Optimization": "snowflake-site:taxonomy/products/search-optimization",
    "Time Travel": "snowflake-site:taxonomy/products/time-travel",
    "Streams & Tasks": "snowflake-site:taxonomy/products/streams-tasks",
    "Dynamic Tables": "snowflake-site:taxonomy/products/dynamic-tables",
    "Snowpark ML": "snowflake-site:taxonomy/products/snowpark-ml",
    "Geo Spatial": "snowflake-site:taxonomy/products/geo-spatial",
    "Data Sharing": "snowflake-site:taxonomy/products/data-sharing",
    "Data Masking": "snowflake-site:taxonomy/products/data-masking",
    "Data Classification": "snowflake-site:taxonomy/products/data-classification",
    "Document AI": "snowflake-site:taxonomy/products/document-ai",
    "Alerts": "snowflake-site:taxonomy/products/alerts",
}

IMAGE_CT_RE = re.compile(r"image/(png|jpeg|jpg|gif|svg|webp|bmp|x-icon)", re.I)


def load_template():
    for path in ("templates/markdown-template.md", "_markdown-template/markdown-template.md"):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return (
        "author: Author Name\n"
        "id: example-guide\n"
        "language: en\n"
        "summary: Example\n"
        "categories: snowflake-site:taxonomy/solution-center/certification/quickstart\n"
        "environments: web\n"
        "status: Published\n"
        "feedback link: https://github.com/Snowflake-Labs/sfguides/issues\n"
        "fork repo link: <repo>\n"
        "open in snowflake: <deeplink>\n\n"
        "# Snowflake Guide Template\n\n## Overview\n...\n"
    )


def validate_markdown(md_text, guide_id):
    issues = []
    # language within first 50 lines and allowed
    first_50 = "\n".join(md_text.splitlines()[:50])
    m = re.search(r"^\s*language:\s*(.+)$", first_50, re.M)
    lang = m.group(1).strip().strip("'\"") if m else ""
    if not lang or lang.lower() not in ALLOWED_LANGS:
        issues.append(f'language must be one of {ALLOWED_LANGS} and in first 50 lines (found "{lang}")')
    # id matches guide_id
    m = re.search(r"^\s*id:\s*(.+)$", md_text, re.M)
    md_id = m.group(1).strip() if m else ""
    if md_id != guide_id:
        issues.append(f'id must match folder/file name "{guide_id}" (found "{md_id}")')
    # categories: allow comma-separated taxonomy paths
    m = re.search(r"^\s*categories:\s*(.+)$", md_text, re.M)
    cats_line = m.group(1).strip() if m else ""
    if not cats_line:
        issues.append('categories must be set (comma-separated taxonomy paths)')
    else:
        paths = [c.strip() for c in cats_line.split(",") if c.strip()]
        if not paths or any(not p.startswith("snowflake-site:taxonomy/") for p in paths):
            issues.append('categories must be comma-separated taxonomy paths (e.g., snowflake-site:taxonomy/solution-center/certification/quickstart)')
    return issues


def sanitize_filename(name):
    base = os.path.basename(name)
    # prefer hyphens, allow . _ -
    base = base.lower().replace("_", "-")
    return re.sub(r"[^a-z0-9_.\-]", "", base)


def write_guide_tree(base_dir, guide_id, md_text, image_files, other_files):
    guide_dir = os.path.join(base_dir, "site", "sfguides", "src", guide_id)
    assets_dir = os.path.join(guide_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(guide_dir, f"{guide_id}.md"), "w", encoding="utf-8") as f:
        f.write(md_text)

    saved = []

    # Images (<= 1MB)
    for up in image_files or []:
        # accept by content-type or extension
        is_image = (up.type and IMAGE_CT_RE.search(up.type)) or re.search(r"\.(png|jpe?g|gif|svg|webp|bmp|ico)$", up.name.lower())
        if not is_image:
            continue
        data = up.getvalue()
        if len(data) > 1_000_000:
            continue
        name = sanitize_filename(up.name)
        p = os.path.join(assets_dir, name)
        with open(p, "wb") as f:
            f.write(data)
        saved.append(("assets/" + name, len(data)))

    # Additional files (any type), cap at 10MB, skip .md
    for up in other_files or []:
        data = up.getvalue()
        if len(data) > 10_000_000:
            continue
        name = sanitize_filename(up.name)
        if not name or name.endswith(".md"):
            continue
        p = os.path.join(assets_dir, name)
        with open(p, "wb") as f:
            f.write(data)
        saved.append(("assets/" + name, len(data)))

    return guide_dir, saved


def zipdir(path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(path):
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, path)
                zf.write(full, rel)
    buf.seek(0)
    return buf


def convert_img_tags_to_markdown(text: str) -> str:
    """Convert basic <img src="..." alt="..."> HTML to Markdown image syntax."""
    if not text:
        return text
    # alt and src
    text = re.sub(
        r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*>',
        r'![\1](\2)',
        text,
        flags=re.IGNORECASE,
    )
    # src only
    text = re.sub(
        r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>',
        r'![](\1)',
        text,
        flags=re.IGNORECASE,
    )
    return text


def fetch_category_map():
    """
    Returns dict of display_label -> taxonomy_path.
    Merges fetched items with EXTENDED_CATEGORIES. Avoids label collisions.
    """
    paths = set()
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Guide-Generator)"}
        r = requests.get(CATEGORIES_SOURCE_URL, headers=headers, timeout=10)
        r.raise_for_status()
        text = r.text
        # Broaden regex: allow A–Z and dots/underscores
        found = set(m.group(0) for m in re.finditer(r"snowflake-site:taxonomy/[A-Za-z0-9/\-_.]+", text))
        paths |= found
    except Exception:
        pass

    # Always merge fallback and extended
    paths |= set(CATEGORIES_FALLBACK.values())

    # Build display labels, avoid collisions by appending parent segment when needed
    by_label = {}
    seen_labels = set()
    for p in sorted(paths):
        parts = [seg for seg in p.split("/") if seg]
        tail = parts[-1] if parts else p
        label = tail.replace("-", " ").title()
        if label in seen_labels and len(parts) >= 2:
            parent = parts[-2].replace("-", " ").title()
            label = f"{parent}: {label}"
        seen_labels.add(label)
        by_label[label] = p

    return by_label

def build_guide_markdown(meta, sections):
    # Metadata block at top (kept within first 50 lines for CI)
    # Sanitize any HTML image tags into markdown
    sections = dict(sections)
    sections["overview"] = convert_img_tags_to_markdown(sections.get("overview") or "")
    sections["build"] = convert_img_tags_to_markdown(sections.get("build") or "")
    sanitized_steps = []
    for s in sections.get("steps") or []:
        sanitized_steps.append({
            "title": (s.get("title") or "").strip(),
            "content": convert_img_tags_to_markdown(s.get("content") or "")
        })
    sections["steps"] = sanitized_steps
    sections["conclusion"] = convert_img_tags_to_markdown(sections.get("conclusion") or "")

    header = [
        f'author: {meta["author"]}',
        f'id: {meta["id"]}',
        f'language: {meta["language"]}',
        f'summary: {meta["summary"]}',
        f'categories: {meta["categories"]}',
        f'environments: {meta["environments"]}',
        f'status: {meta["status"]}',
        f'feedback link: {meta["feedback"]}',
        f'fork repo link: {meta["fork_repo"]}',
        f'open in snowflake: {meta["open_in"]}',
        "",
    ]
    # Lists
    wl = [f"- {x.strip()}" for x in (sections.get("learn") or "").splitlines() if x.strip()]
    wn = [f"- {x.strip()}" for x in (sections.get("need") or "").splitlines() if x.strip()]
    # Resources: "Label | URL" or raw URL
    res_lines = []
    for line in (sections.get("resources") or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if " | " in line:
            label, url = [p.strip() for p in line.split(" | ", 1)]
            res_lines.append(f"- [{label}]({url})")
        else:
            res_lines.append(f"- {line}")
    # Steps
    steps_md = []
    for idx, step in enumerate(sections.get("steps") or [], start=1):
        title = step.get("title", "").strip() or f"Step {idx}"
        content = step.get("content", "").strip()
        steps_md.append(f"## Step {idx}: {title}\n\n{content}")
    process_block = "\n\n".join(steps_md)

    body = []
    body.append(f"# {sections.get('title') or 'Snowflake Guide'}\n")
    body.append("## Overview\n" + (sections.get("overview") or "").strip() + "\n")
    if wl:
        body.append("### What You’ll Learn\n" + "\n".join(wl) + "\n")
    if wn:
        body.append("### What You’ll Need\n" + "\n".join(wn) + "\n")
    if sections.get("build"):
        body.append("### What You’ll Build\n" + sections["build"].strip() + "\n")
    body.append("## Process\n" + (f"{process_block}\n" if process_block else ""))
    if sections.get("conclusion") or res_lines:
        body.append("## Conclusion And Resources\n")
        if sections.get("conclusion"):
            body.append("### Conclusion\n" + sections["conclusion"].strip() + "\n")
        if res_lines:
            body.append("### Related Resources\n" + "\n".join(res_lines) + "\n")
    return "\n".join(header + body)


def list_ai_inputs(base="new-template-form-inputs"):
    md_files = []
    if os.path.isdir(base):
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower().endswith(".md"):
                    md_files.append(os.path.join(root, f))
    return sorted(md_files)


# Theming (dark blue bg, light text; white inputs with dark text) and wide layout
st.set_page_config(page_title="Snowflake Guide Generator", page_icon="❄️", layout="wide")
st.markdown(
    """
    <style>
      :root {
        --bg: #13265C;            /* Dark blue app background */
        --text-light: #F2F5FA;    /* Very light grey for dark bg */
        --text-dark: #111827;     /* Near-black on white bg */
        --white: #ffffff;
        --accent: #29B5E8;        /* Snowflake Blue */
      }

      /* Base layout */
      .stApp { background: var(--bg); color: var(--text-light); }
      .block-container { max-width: 1400px; padding-left: 2rem; padding-right: 2rem; }
      h1, h2, h3 { color: var(--accent) !important; }
      h4 { color: var(--text-light) !important; }
      body, p, li, span, label, [data-testid="stMarkdownContainer"] {
        color: var(--text-light) !important;
      }
      a { color: var(--accent) !important; }

      /* Text inputs/areas: white bg, dark text */
      .stTextInput > div > div,
      .stTextArea  > div > div,
      .stNumberInput > div > div {
        background-color: var(--white) !important;
      }
      .stTextInput input,
      .stTextArea  textarea,
      .stNumberInput input {
        color: var(--text-dark) !important;
        background-color: var(--white) !important;
        border-color: #DFE3E8 !important;
      }

      /* File uploader: white bg, dark text */
      [data-testid="stFileUploader"] section div {
        background-color: var(--white) !important;
        color: var(--text-dark) !important;
      }
      /* Hide default per-file size hint text under uploader */
      [data-testid="stFileUploader"] small { display: none !important; }

      /* Buttons */
      .stButton>button, .stDownloadButton>button {
        background-color: var(--accent) !important;
        color: var(--bg) !important;
        border: none !important;
      }
      /* Submit button (Generate Guide) - larger and light blue */
      .stFormSubmitButton>button {
        background-color: #5EC8F8 !important;
        color: #0B1220 !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.1rem !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
      }

      /* SELECT/MULTISELECT: FORCE DARKER TEXT */

      /* Combobox (visible value/placeholder) */
      .stSelectbox div[role="combobox"],
      .stMultiSelect div[role="combobox"] {
        background: var(--white) !important;
        color: var(--text-dark) !important;
      }
      /* Force darker text inside select value and labels */
      .stSelectbox [data-baseweb="select"] div,
      .stSelectbox [data-baseweb="select"] span,
      .stMultiSelect [data-baseweb="select"] div,
      .stMultiSelect [data-baseweb="select"] span {
        color: var(--text-dark) !important;
      }
      /* Extra enforcement for tricky BaseWeb nodes */
      .stSelectbox div[role="combobox"] *,
      .stMultiSelect div[role="combobox"] * {
        color: var(--text-dark) !important;
        fill: var(--text-dark) !important; /* icons/carets */
      }
      /* Selected single value text */
      .stSelectbox [data-baseweb="select"] [aria-selected="true"],
      .stSelectbox [data-baseweb="select"] [data-baseweb="selected"] {
        color: var(--text-dark) !important;
      }
      /* Placeholder when empty */
      .stSelectbox [data-baseweb="select"] [aria-placeholder="true"],
      .stSelectbox [data-baseweb="select"] [data-placeholder="true"] {
        color: var(--text-dark) !important;
        opacity: 1 !important;
      }

      /* BaseWeb select internals: make every descendant dark */
      .stSelectbox [data-baseweb="select"] *,
      .stMultiSelect [data-baseweb="select"] * {
        color: var(--text-dark) !important;
      }
      /* Selected product tags (chips) */
      .stMultiSelect [data-baseweb="tag"] {
        background: #E6F3FF !important;     /* Snowflake light blue */
        color: #0B2E59 !important;
        border-color: #5EC8F8 !important;
      }
      /* Ensure select containers are white */
      .stSelectbox div[data-baseweb="select"],
      .stSelectbox div[data-baseweb="select"] > div,
      .stSelectbox div[role="combobox"],
      .stMultiSelect div[data-baseweb="select"],
      .stMultiSelect div[data-baseweb="select"] > div,
      .stMultiSelect div[role="combobox"] {
        background-color: var(--white) !important;
      }
      
      /* Input element inside select combobox */
      .stSelectbox [data-baseweb="select"] input,
      .stMultiSelect [data-baseweb="select"] input {
        color: var(--text-dark) !important;
        background: var(--white) !important;
      }

      /* Placeholder inside select */
      .stSelectbox input::placeholder,
      .stMultiSelect input::placeholder {
        color: var(--text-dark) !important;
        opacity: 1 !important;
      }

      /* Dropdown menu and items */
      ul[role="listbox"],
      ul[role="listbox"] li,
      ul[role="listbox"] li * {
        background: var(--white) !important;
        color: var(--text-dark) !important;
      }
      /* Note callout styling */
      .note-callout {
        background: #E6F3FF;
        color: #0B2E59;
        padding: 12px 16px;
        border-left: 4px solid var(--accent);
        border-radius: 6px;
        margin-top: 16px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<h1>Snowflake Guide Generator</h1>', unsafe_allow_html=True)

# Controls outside the form so changes re-render step fields immediately
st.subheader("Process steps")
st.caption("Change the number to add/remove step fields below.")
_col_step_left, _col_step_right = st.columns([1, 2], gap="large")
with _col_step_left:
    st.number_input(
        "Number of steps",
        min_value=1, max_value=20, value=int(st.session_state.get("step_count", 3)),
        step=1, key="step_count"
    )

# Preload categories
categories_map = fetch_category_map()
product_names = sorted(categories_map.keys())

with st.form("guide_form"):
    col_meta, col_right = st.columns([1, 2], gap="large")
    with col_meta:
        st.subheader("Metadata")
        guide_id = st.text_input(
            "Guide ID (folder and filename, hyphen-case)",
            placeholder="intro-to-cortex",
            key="meta_guide_id",
        ).strip()
        author = st.text_input("Author", placeholder="First Last", key="meta_author").strip()
        language = st.selectbox("Language", ALLOWED_LANGS, index=ALLOWED_LANGS.index("en"), key="meta_language")
        summary = st.text_input("Summary (1 sentence)", placeholder="This is a sample Snowflake Guide", key="meta_summary").strip()

        default_products = [product_names[0]] if product_names else []
        selected_products = st.multiselect(
            "Products (choose one or more; Categories will be added as taxonomy paths)",
            product_names,
            default=default_products,
            key="meta_products",
        )
        auto_categories_list = [categories_map[p] for p in selected_products] if selected_products else [CATEGORIES_FALLBACK["Quickstart"]]
        auto_categories = ", ".join(auto_categories_list)
        categories_final = auto_categories

        st.text("Status: Published")
        status = "Published"

        environments = st.text_input("Environments", value="web (default)", key="meta_env").strip()
        feedback = st.text_input("Feedback link", value="https://github.com/Snowflake-Labs/sfguides/issues", key="meta_feedback").strip()
        fork_repo = st.text_input("Fork repo link", value="<repo>", key="meta_forkrepo").strip()
        open_in = st.text_input("Open in Snowflake (if template or deeplink is available)", value="<deeplink or remove>", key="meta_openin").strip()

        st.subheader("Assets")
        image_uploads = st.file_uploader(
            "Upload images (≤ 1MB each; use hyphens in filenames; saved to /assets)",
            type=["png","jpg","jpeg","gif","svg","webp","bmp","ico"],
            accept_multiple_files=True,
            key="assets_images",
        )
        other_uploads = st.file_uploader(
            "Upload additional files (non-images; will be placed in assets/, ≤ 10MB each)",
            accept_multiple_files=True,
            key="assets_other",
        )

        # Publishing Options at the bottom of metadata
        CONTENT_TYPE_OPTIONS = {
            # Reference list; extend as needed based on approved taxonomy
            "Quickstart": "snowflake-site:taxonomy/solution-center/certification/quickstart",
            "Certified Solution": "snowflake-site:taxonomy/technical/certified-solution",
        }
        st.subheader("Publishing Options")
        content_type_choice = st.selectbox(
            "Content Type",
            list(CONTENT_TYPE_OPTIONS.keys()),
            index=0,
            key="meta_content_type",
        )
        feature_flag = st.checkbox("Feature this guide", key="meta_feature")

    with col_right:
        st.subheader("Guide Content")
        guide_title = st.text_input("Guide Title (H1)", placeholder="Getting Started with ...", key="content_title").strip()
        overview = st.text_area("Overview", height=140, key="content_overview")
        learn = st.text_area("What You’ll Learn (one per line)", height=100, key="content_learn")
        need = st.text_area("What You’ll Need (one per line)", height=100, key="content_need")
        build_txt = st.text_input("What You’ll Build", placeholder="Describe the final outcome", key="content_build")

        st.subheader("Steps to include in Guide")
        sc = int(st.session_state.get("step_count", 3))
        steps = []
        for i in range(sc):
            st.markdown(f"#### Step {i+1}")
            title_key = f"steps_title_{i}"
            content_key = f"steps_content_{i}"
            st.text_input(f"Step {i+1} title (3–4 words)", key=title_key)
            st.text_area(f"Step {i+1} content", key=content_key, height=140)
            steps.append({
                "title": st.session_state.get(title_key, "").strip(),
                "content": st.session_state.get(content_key, "").strip()
            })

        st.subheader("Conclusion and Resources")
        conclusion = st.text_area("Concluding Statement", height=120, key="content_conclusion")
        resources = st.text_area("Related resources (one per line; optional 'Label | URL')", height=100, key="content_resources")

        # Merge Content Type and Featured tag into Categories
        selected_ct_path = CONTENT_TYPE_OPTIONS.get(content_type_choice, "")
        extra_tags = []
        if selected_ct_path:
            extra_tags.append(selected_ct_path)
        if feature_flag:
            extra_tags.append("snowflake-site:taxonomy/technical/featured")
        if extra_tags:
            categories_final = ", ".join([categories_final] + extra_tags)

        # Right-align the Generate Guide button
        btn_spacer, btn_col = st.columns([3, 1])
        with btn_col:
            submitted = st.form_submit_button("Generate Guide")

if submitted:
    if not guide_id or not re.match(r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$", guide_id):
        st.error("Guide ID required (lowercase letters/numbers with hyphens).")
        st.stop()

    # Build full guide markdown (not just a template)
    meta = {
        "author": author or "First Last",
        "id": guide_id,
        "language": language,
        "summary": summary or "This is a sample Snowflake Guide",
        "categories": categories_final,
        "environments": environments or "web",
        "status": status,
        "feedback": feedback,
        "fork_repo": fork_repo,
        "open_in": open_in
    }
    # remove completely empty steps; keep all others
    steps_filtered = [s for s in steps if (s.get("title","") or s.get("content",""))]
    sections = {
        "title": guide_title,
        "overview": overview,
        "learn": learn,
        "need": need,
        "build": build_txt,
        "steps": steps_filtered,
        "conclusion": conclusion,
        "resources": resources
    }
    md = build_guide_markdown(meta, sections)

    issues = validate_markdown(md, guide_id)
    if issues:
        st.warning("Validation issues (key CI checks):\n- " + "\n- ".join(issues))
    else:
        st.success("Local validation passed (key checks).")

    with tempfile.TemporaryDirectory() as td:
        guide_dir, saved = write_guide_tree(td, guide_id, md, image_uploads or [], other_uploads or [])
        if saved:
            st.caption("Saved assets: " + ", ".join([f"{n} ({s} bytes)" for n,s in saved]))
        buf = zipdir(guide_dir)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download Guide ZIP",
            data=buf,
            file_name=f"{guide_id}_{ts}.zip",
            mime="application/zip"
        )

st.markdown(
    '<div class="note-callout">Next: unzip into your fork of the sfguides repo at site/sfguides/src/&lt;guide-id&gt;/, modify or update the markdown file as needed, open PR, and submit. Your guide goes through basic validation checks which are built in.</div>',
    unsafe_allow_html=True,
)

