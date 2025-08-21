import base64
from io import BytesIO
from pathlib import Path
from datetime import date

import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa

# ---------- Paths ----------
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"

# ---------- Utilities ----------
def render_html(context: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("proposal_template.html")
    return template.render(**context)

def html_to_pdf_bytes(html: str) -> bytes:
    """Convert HTML to PDF in-memory using xhtml2pdf."""
    pdf_io = BytesIO()
    result = pisa.CreatePDF(src=html, dest=pdf_io, encoding="utf-8")
    if result.err:
        raise RuntimeError("PDF generation failed. Check HTML/CSS compatibility.")
    return pdf_io.getvalue()

def image_file_to_data_uri(file) -> str | None:
    if not file:
        return None
    data = file.read()
    mime = file.type or "image/png"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Proposal Generator", page_icon="📄", layout="wide")
st.title("📄 Freelance Proposal Generator")
st.caption("Fill the form, preview instantly, and export to PDF/HTML.")

with st.sidebar:
    st.header("⚙️ Settings")
    accent = st.selectbox("Accent Style", ["Black & White", "Minimal Gray", "Classic Serif"])
    include_tos = st.toggle("Include Terms & Acceptance", value=True)
    show_page_numbers = st.toggle("Show Page Numbers", value=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Client")
    client_name = st.text_input("Client name", value="Acme Corp")
    client_contact = st.text_input("Client contact (email/phone)", value="jane@acme.com | +1 (555) 555-0199")
    client_address = st.text_area("Client address", value="123 Market St\nCity, ST 12345")

with col2:
    st.subheader("Your info")
    sender_name = st.text_input("Your/Company name", value="Price DevOps")
    sender_email = st.text_input("Your email", value="hello@pricedevops.io")
    sender_phone = st.text_input("Your phone", value="(555) 867-5309")

logo_file = st.file_uploader("Upload a logo (optional)", type=["png", "jpg", "jpeg", "webp"])
sign_file = st.file_uploader("Upload a signature (optional)", type=["png", "jpg", "jpeg", "webp"])

st.divider()
st.subheader("Project Details")

project_title = st.text_input("Project title", value="Website Redesign & Optimization")
summary = st.text_area(
    "Executive summary",
    value=(
        "We will redesign the client's marketing site with a clean black & white aesthetic, "
        "improve conversion UX, and automate proposal generation."
    ),
)

col3, col4 = st.columns(2)
with col3:
    scope_items = st.text_area(
        "Scope (one per line)",
        value="Discovery workshop\nHigh-fidelity UI in Figma\nResponsive frontend (Next.js)\nBasic SEO + analytics\nLaunch & handoff",
        height=140,
    )
with col4:
    deliverables = st.text_area(
        "Deliverables (one per line)",
        value="Design system tokens\nComponent library\nSEO report\nDeployment playbook",
        height=140,
    )

timeline = st.text_input("Timeline", value="4–6 weeks")
price = st.text_input("Price", value="$6,500 fixed")
valid_until = st.date_input("Quote valid until", value=date.today())
payment_terms = st.text_area("Payment terms", value="50% upfront, 25% mid-project, 25% on delivery.")
notes = st.text_area("Notes (optional)", value="Weekly updates each Friday. Slack for daily comms.")

# ---------- Build context ----------
context = {
    "accent": accent,
    "include_tos": include_tos,
    "show_page_numbers": show_page_numbers,
    "client": {
        "name": client_name,
        "contact": client_contact,
        "address": client_address,
    },
    "sender": {
        "name": sender_name,
        "email": sender_email,
        "phone": sender_phone,
    },
    "project": {
        "title": project_title,
        "summary": summary,
        "scope": [s for s in scope_items.splitlines() if s.strip()],
        "deliverables": [d for d in deliverables.splitlines() if d.strip()],
        "timeline": timeline,
        "price": price,
        "valid_until": valid_until.strftime("%B %d, %Y"),
        "payment_terms": payment_terms,
        "notes": notes,
    },
    "assets": {
        "logo_data_uri": image_file_to_data_uri(logo_file),
        "sign_data_uri": image_file_to_data_uri(sign_file),
    },
}

# ---------- Render & Preview ----------
html = render_html(context)

st.subheader("Preview")
st.components.v1.html(html, height=900, scrolling=True)

# ---------- Downloads ----------
st.divider()
col_a, col_b = st.columns(2)

with col_a:
    st.download_button(
        "⬇️ Download HTML",
        data=html.encode("utf-8"),
        file_name="proposal.html",
        mime="text/html",
    )

with col_b:
    try:
        pdf_bytes = html_to_pdf_bytes(html)
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes,
            file_name="proposal.pdf",
            mime="application/pdf",
        )
    except Exception:
        st.warning(
            "PDF export failed on this platform. You can still download HTML and print to PDF from your browser."
        )
