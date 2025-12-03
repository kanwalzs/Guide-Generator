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
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def inject_metadata(template_text, meta):
    def repl(txt, key, value):
        pat = re.compile(rf"^{re.escape(key)}:\s*.*$", re.M)
        if pat.search(txt):
            return pat.sub(f"{key}: {value}", txt)
        return f"{key}: {value}\n{txt}"
    text = template_text
    for k, v in meta.items():
        text = repl(text, k, v)
    return text

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

# Theming (white bg, Snowflake Blue headings)
st.set_page_config(page_title="Snowflake Guide Generator", page_icon="❄️", layout="centered")
st.markdown(
   """
    <style>
      :root {
        --bg: #0B1220;           /* Dark background */
        --text-primary: #F5F7FA; /* Near-white */
        --text-secondary: #E5E7EB; /* Light grey */
        --accent: #29B5E8;       /* Snowflake Blue */
        --input-bg: #0F172A; 
        --border: #1F2937;
      }
      .stApp { background-color: var(--bg); color: var(--text-primary); }

      /* Headings */
      h1, h2, h3 { color: var(--accent) !important; }

      /* General text */
      body, p, li, span, div, label, [data-testid="stMarkdownContainer"] {
        color: var(--text-secondary) !important;
      }
      a { color: var(--accent) !important; }

      /* Inputs and textareas */
      input, textarea, select {
        color: var(--text-primary) !important;
        background-color: var(--input-bg) !important;
        border-color: var(--border) !important;
      }

      /* Buttons */
      .stButton>button, .stDownloadButton>button {
        background-color: var(--accent) !important;
        color: #0B1220 !important;
        border: none !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<h1>Snowflake Guide Generator</h1>', unsafe_allow_html=True)

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
        "Products (choose one or more; auto-fills taxonomy paths)",
        product_names,
        default=default_products
    )
    auto_categories_list = [categories_map[p] for p in selected_products] if selected_products else [CATEGORIES_FALLBACK["Quickstart"]]
    auto_categories = ", ".join(auto_categories_list)
    override = st.checkbox("Override categories (advanced)", value=False)
    categories_input = st.text_input(
        "Categories (taxonomy paths, comma-separated)",
        value=auto_categories,
        disabled=not override
    ).strip()
    categories_final = categories_input if override else auto_categories

    # Status (no 'Hidden')
    status = st.selectbox("Status", ["Published", "Archived"], index=0)
    environments = st.text_input("Environments", value="web").strip()
    feedback = st.text_input("Feedback link", value="https://github.com/Snowflake-Labs/sfguides/issues").strip()
    fork_repo = st.text_input("Fork repo link", value="<repo>").strip()
    open_in = st.text_input("Open in Snowflake", value="<deeplink or remove>").strip()

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

    tmpl = load_template()
    md = inject_metadata(tmpl, {
        "author": author or "First Last",
        "id": guide_id,
        "language": language,
        "summary": summary or "This is a sample Snowflake Guide",
        "categories": categories_final,
        "environments": environments or "web",
        "status": status,
        "feedback link": feedback,
        "fork repo link": fork_repo,
        "open in snowflake": open_in
    })

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

st.info("Next: unzip into your guide repo at site/sfguides/src/<guide-id>/, open PR, and let CI validate.")