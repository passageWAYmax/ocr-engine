import os
import json
import streamlit as st
from PIL import Image

from main import run_ocr


# ------------------ CACHE OCR ------------------
@st.cache(show_spinner=False, allow_output_mutation=True)
def cached_ocr(image_path: str):
    return run_ocr(image_path)


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="OCR Engine",
    layout="wide"
)


# ------------------ THEME / CSS ------------------
st.markdown("""
<style>
.stApp {
    background-color: #FBFDFF;
    color: #0F172A;
}

h1, h2, h3 {
    color: #2563EB !important;
    font-weight: 700 !important;
}

label, p {
    color: #0F172A !important;
    font-weight: 500;
}

header[data-testid="stHeader"] {
    background-color: #2563EB !important;
}
header[data-testid="stHeader"] * {
    color: #FFFFFF !important;
}

div[data-testid="stAlert"] {
    background-color: #D1FAE5 !important;
    border-left: 5px solid #059669 !important;
    border-radius: 8px;
}
div[data-testid="stAlert"] * {
    color: #064E3B !important;
    font-weight: 700 !important;
}

div[data-testid="stImage"] button {
    display: none !important;
}

button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
button:hover {
    background-color: #1E40AF !important;
}

/* RIGHT COLUMN SCROLL */

div[data-testid="column"]:nth-of-type(2) > div > div > div {
    max-height: 80vh;
    overflow-y: auto;
    padding-right: 10px;
}

/* scrollbar styling */
div[data-testid="column"]:nth-of-type(2) ::-webkit-scrollbar {
    width: 8px;
}

div[data-testid="column"]:nth-of-type(2) ::-webkit-scrollbar-thumb {
    background-color: #94A3B8;
    border-radius: 10px;
}

div[data-testid="column"]:nth-of-type(2) ::-webkit-scrollbar-track {
    background-color: #E5E7EB;
}
            
</style>
""", unsafe_allow_html=True)


# ------------------ HEADER ------------------
st.title("OCR ENGINE")
st.caption("Offline OCR & Document Intelligence (PaddleOCR + Gemini_3)")


# ------------------ MAIN LAYOUT ------------------
left_col, right_col = st.columns([1, 1.4])


# ------------------ LEFT COLUMN ------------------
with left_col:
    st.subheader("📤 Upload Document Image")

    uploaded_file = st.file_uploader(
        "Upload image (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"]
    )

    image_path = None

    if uploaded_file:
        os.makedirs("images", exist_ok=True)
        image_path = os.path.join("images", uploaded_file.name)

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        image = Image.open(image_path)

        st.subheader("🖼 Image Preview")
        st.image(image, width=360)


# ------------------ OCR PROCESS ------------------
result = None

if image_path:
    with st.spinner("🔍 Running OCR + AI parsing..."):
        try:
            result = cached_ocr(image_path)
        except Exception as e:
            st.error(f"OCR failed: {e}")
            result = None


# ------------------ RIGHT COLUMN ------------------
with right_col:
    if result and isinstance(result, dict):

       scroll_container = st.container()

       with scroll_container:
        st.success("✅ Processing completed successfully")

        boxed_image_path = result.get("boxed_image_path")
        if boxed_image_path and os.path.exists(boxed_image_path):
            st.subheader("📦 Detected Text Regions")
            st.image(boxed_image_path, use_column_width=True)

        parsed_data = result.get("parsed_data")

        if parsed_data:
            st.subheader("🧾 Extracted Document Data")

            for key, value in parsed_data.items():
                if isinstance(value, list):
                    st.markdown(f"### {key.replace('_', ' ').title()}")
                    if value:
                        st.table(value)
                    else:
                        st.info(f"No {key} detected")
                elif isinstance(value, dict):
                    st.markdown(f"### {key.replace('_', ' ').title()}")
                    st.json(value)
                else:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

        else:
            st.warning("No structured data could be extracted from this document.")

        structured_data = result.get("llm_output", {})

        with st.expander("📋 View Extracted Data (JSON)", expanded=True):
            st.json(structured_data)

        st.subheader("⬇ Download Output")

        st.download_button(
            "📥 Download Full JSON",
            data=json.dumps(result, indent=4, ensure_ascii=False),
            file_name="ocr_output.json",
            mime="application/json"
        )
