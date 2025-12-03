import streamlit as st
import os, io, re, shutil, tempfile, zipfile
from datetime import datetime

ALLOWED_LANGS = ["en","es","it","fr","de","ja","ko","pt_br"]

def load_template(path="templates/markdown-template.md"):
    if not os.path.exists(path):
        return "author: Author Name\nid: example-guide\nlanguage: en\nsummary: Example\ncategories: snowflake-site:taxonomy/solution-center/certification/quickstart\nenvironments: web\nstatus: Published\nfeedback link: https://github.com/Snowflake-Labs/sfguides/issues\nfork repo link: <repo>\nopen in snowflake: <deeplink>\n\n# Snowflake Guide Template\n\n## Overview\n...\n"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def inject_metadata(template_text, meta):
    def repl(line, key, value):
        pat = re.compile(rf"^{re.escape(key)}:\s*.*$", re.M)
        if pat.search(line):
            return pat.sub(f"{key}: {value}", line)
        return f"{key}: {value}\n{line}"
    text = template_text
    for k,v in meta.items():
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

    # id present and matches guide_id
    m = re.search(r"^\s*id:\s*(.+)$", md_text, re.M)
    md_id = m.group(1).strip() if m else ""
    if md_id != guide_id:
        issues.append(f'id must match folder/file name "{guide_id}" (found "{md_id}")')

    # categories present and non-empty (light check)
    m = re.search(r"^\s*categories:\s*(.+)$", md_text, re.M)
    cats = m.group(1).strip() if m else ""
    if not cats or ":" not in cats:
        issues.append('categories must be set (ex: snowflake-site:taxonomy/solution-center/certification/quickstart)')

    return issues

def write_guide_tree(base_dir, guide_id, md_text, assets):
    guide_dir = os.path.join(base_dir, "site", "sfguides", "src", guide_id)
    assets_dir = os.path.join(guide_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(guide_dir, f"{guide_id}.md"), "w", encoding="utf-8") as f:
        f.write(md_text)
    saved = []
    for up in assets:
        # validate image type + size <= 1MB
        if not up.type or not re.search(r"image/(png|jpeg|jpg|gif|svg|webp|bmp|x-icon)", up.type, re.I):
            continue
        if len(up.getvalue()) > 1_000_000:
            continue
        # normalize filename: lowercase underscores
        name = re.sub(r"[^a-z0-9_.]", "", up.name.lower().replace("-", "_"))
        p = os.path.join(assets_dir, name)
        with open(p, "wb") as f:
            f.write(up.getbuffer())
        saved.append(("assets/"+name, len(up.getvalue())))
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

st.set_page_config(page_title="Snowflake Guide Generator", page_icon="❄️", layout="centered")
st.title("Snowflake Guide Generator")

with st.form("guide_form"):
    st.subheader("Metadata")
    guide_id = st.text_input("Guide ID (folder and filename, hyphen-case)", placeholder="intro-to-cortex").strip()
    author = st.text_input("Author", placeholder="First Last").strip()
    language = st.selectbox("Language", ALLOWED_LANGS, index=0)
    summary = st.text_input("Summary (1 sentence)", placeholder="This is a sample Snowflake Guide").strip()
    categories = st.text_input("Categories", value="snowflake-site:taxonomy/solution-center/certification/quickstart").strip()
    status = st.selectbox("Status", ["Published", "Archived", "Hidden"], index=0)
    environments = st.text_input("Environments", value="web").strip()
    feedback = st.text_input("Feedback link", value="https://github.com/Snowflake-Labs/sfguides/issues").strip()
    fork_repo = st.text_input("Fork repo link", value="<repo>").strip()
    open_in = st.text_input("Open in Snowflake", value="<deeplink or remove>").strip()

    st.subheader("Assets")
    uploads = st.file_uploader("Upload images (<= 1MB each; lowercase_underscores.png)", type=["png","jpg","jpeg","gif","svg","webp","bmp","ico"], accept_multiple_files=True)

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
        "categories": categories,
        "environments": environments or "web",
        "status": status,
        "feedback link": feedback,
        "fork repo link": fork_repo,
        "open in snowflake": open_in
    })

    issues = validate_markdown(md, guide_id)
    if issues:
        st.warning("Validation issues (mirror key CI checks):\n- " + "\n- ".join(issues))
    else:
        st.success("Local validation passed (key checks).")

    with tempfile.TemporaryDirectory() as td:
        guide_dir, saved = write_guide_tree(td, guide_id, md, uploads or [])
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
