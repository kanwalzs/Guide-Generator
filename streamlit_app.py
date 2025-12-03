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
    return re.sub(r"[^a-z0-9_.]", "", base.lower().replace("-", "_"))


def write_guide_tree(base_dir, guide_id, md_text, image_files, other_files, url_files):
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

    # URL downloads (any type), cap at 10MB, skip .md
    for url in url_files or []:
        try:
            r = requests.get(url, timeout=10, stream=True)
            r.raise_for_status()
            data = r.content
            if len(data) > 10_000_000:
                continue
            guessed = os.path.basename(urlparse(url).path) or "download"
            name = sanitize_filename(guessed)
            if not name or name.endswith(".md"):
                continue
            p = os.path.join(assets_dir, name)
            with open(p, "wb") as f:
                f.write(data)
            saved.append(("assets/" + name, len(data)))
        except Exception:
            continue

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


def fetch_category_map():
    # Try to scrape taxonomy paths from the referenced doc; fallback if anything fails
    try:
        r = requests.get(CATEGORIES_SOURCE_URL, timeout=10)
        r.raise_for_status()
        text = r.text
        paths = sorted(set(m.group(0) for m in re.finditer(r"snowflake-site:taxonomy/[a-z0-9/\-_]+", text)))
        mapping = {}
        for p in paths:
            # Use last segment as label; title-case for display
            label = p.split("/")[-1].replace("-", " ").title()
            mapping[label] = p
        return mapping or CATEGORIES_FALLBACK
    except Exception:
        return CATEGORIES_FALLBACK


def build_guide_markdown(meta, sections):
    # Metadata block at top (kept within first 50 lines for CI)
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


# Theming (black bg, light grey text; white inputs with black text)
st.set_page_config(page_title="Snowflake Guide Generator", page_icon="❄️", layout="centered")
st.markdown(
    """
    <style>
      :root {
        --bg: #000000;            /* App background */
        --text-light: #E5E7EB;    /* Light grey on dark bg */
        --text-dark: #111827;     /* Near-black on white bg */
        --white: #ffffff;
        --accent: #29B5E8;        /* Snowflake Blue */
      }

      /* Base layout */
      .stApp { background: var(--bg); color: var(--text-light); }
      h1, h2, h3 { color: var(--accent) !important; }
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

      /* Buttons */
      .stButton>button, .stDownloadButton>button {
        background-color: var(--accent) !important;
        color: var(--bg) !important;
        border: none !important;
      }

      /* SELECT/MULTISELECT: FORCE DARKER TEXT */

      /* Combobox (visible value/placeholder) */
      .stSelectbox div[role="combobox"],
      .stMultiSelect div[role="combobox"] {
        background: var(--white) !important;
        color: var(--text-dark) !important;
      }

      /* BaseWeb select internals: make every descendant dark */
      .stSelectbox [data-baseweb="select"] *,
      .stMultiSelect [data-baseweb="select"] * {
        color: var(--text-dark) !important;
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
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<h1>Snowflake Guide Generator</h1>', unsafe_allow_html=True)

# Controls outside the form so changes re-render step fields immediately
st.subheader("Process steps")
st.caption("Change the number to add/remove step fields below.")
st.number_input(
    "Number of steps",
    min_value=1, max_value=20, value=int(st.session_state.get("step_count", 3)),
    step=1, key="step_count"
)

# Preload categories
categories_map = fetch_category_map()
product_names = sorted(categories_map.keys())

with st.form("guide_form"):
    st.subheader("Metadata")
    guide_id = st.text_input("Guide ID (folder and filename, hyphen-case)", placeholder="intro-to-cortex").strip()
    author = st.text_input("Author", placeholder="First Last").strip()
    language = st.selectbox("Language", ALLOWED_LANGS, index=0)
    summary = st.text_input("Summary (1 sentence)", placeholder="This is a sample Snowflake Guide").strip()

    # Multi-select products -> auto-fill taxonomy paths (comma-separated)
    default_products = [product_names[0]] if product_names else []
    selected_products = st.multiselect(
        "Products (choose one or more; Categories will be added in this format with complete path- taxonomy paths, comma-separated)",
        product_names,
        default=default_products
    )
    auto_categories_list = [categories_map[p] for p in selected_products] if selected_products else [CATEGORIES_FALLBACK["Quickstart"]]
    auto_categories = ", ".join(auto_categories_list)


    # Status (no 'Hidden')
    status = st.text_input("Status", value="Published", disabled=True)
    status = "Published"
    environments = st.text_input("Environments", value="web").strip()
    feedback = st.text_input("Feedback link", value="https://github.com/Snowflake-Labs/sfguides/issues").strip()
    fork_repo = st.text_input("Fork repo link", value="<repo>").strip()
    open_in = st.text_input("Open in Snowflake (if template or deeplink is available)", value="<deeplink or remove>").strip()

    # Use the externally-controlled step count to render fields
    sc = int(st.session_state.get("step_count", 3))
    steps = []
    key_prefix = f"{guide_id or 'guide'}"
    for i in range(sc):
        st.markdown(f"#### Step {i+1}")
        s_title = st.text_input(f"Step {i+1} title", key=f"{key_prefix}_step_title_{i}")
        s_content = st.text_area(f"Step {i+1} content", key=f"{key_prefix}_step_content_{i}", height=140)
        steps.append({"title": s_title, "content": s_content})



    conclusion = st.text_area("Conclusion", height=100)
    resources = st.text_area("Resource links (one per line; optional 'Label | URL')", height=100)

    st.subheader("Assets")
    image_uploads = st.file_uploader(
        "Upload images (<= 1MB each; lowercase_underscores.png)",
        type=["png","jpg","jpeg","gif","svg","webp","bmp","ico"],
        accept_multiple_files=True
    )
    other_uploads = st.file_uploader(
        "Upload additional files (non-images; will be placed in assets/, ≤ 10MB each)",
        accept_multiple_files=True
    )
    url_block = st.text_area(
        "Additional asset URLs (one per line; downloaded into assets/, ≤ 10MB each)",
        placeholder="https://example.com/file.csv\nhttps://example.com/archive.zip"
    )

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
    steps_filtered = [s for s in steps if (s.get("title","").strip() or s.get("content","").strip())]
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

    url_list = [u.strip() for u in (url_block or "").splitlines() if u.strip()]
    with tempfile.TemporaryDirectory() as td:
        guide_dir, saved = write_guide_tree(td, guide_id, md, image_uploads or [], other_uploads or [], url_list)
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

st.info("Next: unzip into your fork of the sfguides repo at site/sfguides/src/<guide-id>/, modify or update the markdown file as needed, open PR, and submit.  Your guide goes through some validation basic checks which are built in.")

st.divider()
with st.expander("AI draft (optional)", expanded=False):
    ai_files = list_ai_inputs()
    if not ai_files:
        st.caption("No input files found under new-template-form-inputs/")
    else:
        ai_choice = st.selectbox("Select input file for AI draft", ai_files, index=0, key="ai_choice")
        run_ai = st.button("Run AI draft with selected input")
        if run_ai:
            try:
                import subprocess, shlex
                template_id = guide_id if guide_id else "preview-id"
                cmd = f'sf ai claude -- --dangerously-skip-permissions -p "Follow instructions from prompts/new-template-generation.md to generate a new template (template id: {template_id}) for the user inputs in {ai_choice}" --verbose --output-format stream-json'
                output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, timeout=300)
                text = output.decode("utf-8", errors="replace")
                st.success("AI draft completed. Raw output shown below.")
                st.text_area("AI output (stream-json)", text, height=240)
                st.info("Copy useful content into the fields above, or add parsing to auto-fill.")
            except Exception as e:
                st.error(f"AI draft failed: {e}")