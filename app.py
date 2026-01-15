import os
import json
import streamlit as st
from PIL import Image

from main import run_ocr

@st.cache(show_spinner=False, allow_output_mutation=True)
def cached_ocr(image_path):
    return run_ocr(image_path)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="OCR Engine (PaddleOCR)",
    layout="wide"
)

# ------------------ THEME / CSS ------------------
# st.markdown("""
# <style>
# .stApp {
#     background-color: #0E1117;
# }

# h1, h2, h3 {
#     color: #2ECC71;
# }

# textarea {
#     background-color: #1C1F26 !important;
#     color: #FAFAFA !important;
#     border-radius: 10px;
#     border: 1px solid #2ECC71 !important;
# }

# button {
#     border-radius: 10px !important;
# }

# div[data-testid="stAlert"] {
#     background-color: #123D2B !important;
#     border-left: 6px solid #2ECC71 !important;
#     color: #FAFAFA !important;
#     border-radius: 12px;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>
# /* ---------------------------------------------------------------------
#    1. GLOBAL PAGE STYLING
# --------------------------------------------------------------------- */
# .stApp {
#     background-color: #FBFDFF;
#     color: #0F172A;
# }

# h1, h2, h3 {
#     color: #2563EB !important;
#     font-weight: 700 !important;
# }

# label, .stText, p {
#     color: #0F172A !important;
#     font-weight: 500;
# }

# /* ---------------------------------------------------------------------
#    2. TOP HEADER BAR (Blue + White Text)
# --------------------------------------------------------------------- */
# header[data-testid="stHeader"] {
#     background-color: #2563EB !important;
# }
# header[data-testid="stHeader"] * {
#     color: #FFFFFF !important;
#     fill: #FFFFFF !important;
# }

# /* ---------------------------------------------------------------------
#    3. SUCCESS BOX (Green Background + Readable Dark Text)
# --------------------------------------------------------------------- */
# div[data-testid="stAlert"] {
#     background-color: #D1FAE5 !important;
#     border: 1px solid #34D399 !important;
#     border-left: 5px solid #059669 !important;
#     border-radius: 8px;
# }
# /* Force text to be dark */
# div[data-testid="stAlert"] * {
#     color: #064E3B !important;
#     font-weight: 700 !important;
# }
# div[data-testid="stAlert"] svg {
#     fill: #059669 !important;
#     color: #059669 !important;
# }

# /* ---------------------------------------------------------------------
#    4. COLUMN SEPARATOR (New!)
# --------------------------------------------------------------------- */
# /* This targets the first column (Left Pane) only */
# @media (min-width: 640px) {
#     div[data-testid="column"]:nth-of-type(1) {
#         border-right: 2px solid #E2E8F0; /* The Vertical Line */
#         padding-right: 3rem;             /* Space between content and line */
#     }
# }

# /* ---------------------------------------------------------------------
#    5. INPUTS & BUTTONS
# --------------------------------------------------------------------- */
# section[data-testid="stFileUploader"] {
#     background-color: #FFFFFF;
#     border: 2px dashed #2563EB;
#     border-radius: 12px;
#     padding: 15px;
# }
# textarea {
#     background-color: #FFFFFF !important;
#     color: #0F172A !important;
#     border: 1px solid #2563EB !important;
#     border-radius: 8px;
# }
# button {
#     background-color: #2563EB !important;
#     color: #FFFFFF !important;
#     border: none !important;
#     border-radius: 8px !important;
# }
# button:hover {
#     background-color: #1E40AF !important;
# }

# /* ---------------------------------------------------------------------
#    6. IMAGE HOVER
# --------------------------------------------------------------------- */
# div[data-testid="stImage"] img {
#     transition: transform 0.3s ease;
#     border-radius: 8px;
#     display: block;
# }
# div[data-testid="stImage"] img:hover {
#     transform: scale(1.03);
#     z-index: 999;
#     box-shadow: 0 10px 20px rgba(0,0,0,0.15);
# }

# </style>
# """, unsafe_allow_html=True)


# st.markdown("""
# <style>
# /* ---------------------------------------------------------------------
#    1. GLOBAL PAGE STYLING
# --------------------------------------------------------------------- */
# .stApp {
#     background-color: #FBFDFF;
#     color: #0F172A;
# }

# h1, h2, h3 {
#     color: #2563EB !important;
#     font-weight: 700 !important;
# }

# label, .stText, p {
#     color: #0F172A !important;
#     font-weight: 500;
# }

# /* ---------------------------------------------------------------------
#    2. TOP HEADER BAR (Blue + White Text)
# --------------------------------------------------------------------- */
# header[data-testid="stHeader"] {
#     background-color: #2563EB !important;
# }
# header[data-testid="stHeader"] * {
#     color: #FFFFFF !important;
#     fill: #FFFFFF !important;
# }

# /* ---------------------------------------------------------------------
#    3. SUCCESS BOX (Green Background + Readable Dark Text)
# --------------------------------------------------------------------- */
# div[data-testid="stAlert"] {
#     background-color: #D1FAE5 !important;
#     border: 1px solid #34D399 !important;
#     border-left: 5px solid #059669 !important;
#     border-radius: 8px;
# }
# div[data-testid="stAlert"] * {
#     color: #064E3B !important; /* Dark Green Text */
#     font-weight: 700 !important;
# }
# div[data-testid="stAlert"] svg {
#     fill: #059669 !important;
#     color: #059669 !important;
# }

# /* ---------------------------------------------------------------------
#    4. COLUMN SEPARATOR
# --------------------------------------------------------------------- */
# @media (min-width: 640px) {
#     div[data-testid="column"]:nth-of-type(1) {
#         border-right: 2px solid #E2E8F0;
#         padding-right: 3rem;
#     }
# }

# /* ---------------------------------------------------------------------
#    5. IMAGE CONTAINER FIX (The "Shrink Wrap" Fix)
# --------------------------------------------------------------------- */
# /* This forces the container to shrink to the image size, 
#    pulling the expand button closer to the image */
# div[data-testid="stImage"] {
#     width: fit-content !important; 
#     max-width: 100% !important;
#     display: block;
# }

# /* ---------------------------------------------------------------------
#    6. IMAGE HOVER (Zoom Effect)
# --------------------------------------------------------------------- */
# div[data-testid="stImage"] img {
#     transition: transform 0.3s ease;
#     border-radius: 8px;
#     display: block;
# }
# div[data-testid="stImage"] img:hover {
#     transform: scale(1.03);
#     z-index: 999;
#     box-shadow: 0 10px 20px rgba(0,0,0,0.15);
# }

# /* ---------------------------------------------------------------------
#    7. INPUTS & BUTTONS
# --------------------------------------------------------------------- */
# section[data-testid="stFileUploader"] {
#     background-color: #FFFFFF;
#     border: 2px dashed #2563EB;
#     border-radius: 12px;
#     padding: 15px;
# }
# textarea {
#     background-color: #FFFFFF !important;
#     color: #0F172A !important;
#     border: 1px solid #2563EB !important;
#     border-radius: 8px;
# }
# button {
#     background-color: #2563EB !important;
#     color: #FFFFFF !important;
#     border: none !important;
#     border-radius: 8px !important;
# }
# button:hover {
#     background-color: #1E40AF !important;
# }

# </style>
# """, unsafe_allow_html=True)


st.markdown("""
<style>
/* ---------------------------------------------------------------------
   1. GLOBAL PAGE STYLING
--------------------------------------------------------------------- */
.stApp {
    background-color: #FBFDFF;
    color: #0F172A;
}

h1, h2, h3 {
    color: #2563EB !important;
    font-weight: 700 !important;
}

label, .stText, p {
    color: #0F172A !important;
    font-weight: 500;
}

/* ---------------------------------------------------------------------
   2. TOP HEADER BAR (Blue + White Text)
--------------------------------------------------------------------- */
header[data-testid="stHeader"] {
    background-color: #2563EB !important;
}
header[data-testid="stHeader"] * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* ---------------------------------------------------------------------
   3. SUCCESS BOX (Green Background + Readable Dark Text)
--------------------------------------------------------------------- */
div[data-testid="stAlert"] {
    background-color: #D1FAE5 !important;
    border: 1px solid #34D399 !important;
    border-left: 5px solid #059669 !important;
    border-radius: 8px;
}
div[data-testid="stAlert"] * {
    color: #064E3B !important;
    font-weight: 700 !important;
}
div[data-testid="stAlert"] svg {
    fill: #059669 !important;
    color: #059669 !important;
}

/* ---------------------------------------------------------------------
   4. COLUMN SEPARATOR
--------------------------------------------------------------------- */
@media (min-width: 640px) {
    div[data-testid="column"]:nth-of-type(1) {
        border-right: 2px solid #E2E8F0;
        padding-right: 3rem;
    }
}

/* ---------------------------------------------------------------------
   5. IMAGE STYLING & BUTTON REMOVAL
--------------------------------------------------------------------- */
/* REMOVE the Enlarge/Fullscreen Button */
div[data-testid="stImage"] button {
    display: none !important;
    pointer-events: none !important;
}

/* Zoom Effect on Hover */
div[data-testid="stImage"] img {
    transition: transform 0.3s ease;
    border-radius: 8px;
    display: block;
}
div[data-testid="stImage"] img:hover {
    transform: scale(1.03);
    z-index: 999;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

/* ---------------------------------------------------------------------
   6. INPUTS & BUTTONS
--------------------------------------------------------------------- */
section[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 2px dashed #2563EB;
    border-radius: 12px;
    padding: 15px;
}
textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px;
}
button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}
button:hover {
    background-color: #1E40AF !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title("OCR ENGINE")
st.caption("Offline OCR powered by PaddleOCR")

# ------------------ MAIN LAYOUT ------------------
left_col, right_col = st.columns([1, 1])

# ------------------ LEFT COLUMN (UPLOAD + PREVIEW) ------------------
with left_col:
    st.subheader("📤 Upload Image")

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
        st.image(image, width=350)

# ------------------ OCR PROCESS ------------------
result = None

if image_path:
    with st.spinner("🔍 Processing image..."):
        try:
            result = cached_ocr(image_path)
        except Exception as e:
            st.error(f"OCR failed: {e}")
            result = None

# ------------------ RIGHT COLUMN (RESULTS) ------------------
with right_col:
    if result and isinstance(result, dict):
        st.success("✅ OCR completed successfully!")

        st.subheader("📄 Extracted Result")

        fields = result.get("fields", {})

        if fields:
            extracted_text = "\n".join(
                f"{k}: {v}" for k, v in fields.items()
            )
        else:
            extracted_text = ""

        st.text_area(
            "Extracted Text",
            value=extracted_text,
            height=280
        )

        st.subheader("⬇ Download Output")

        json_data = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        text_data = extracted_text or "No text detected."

        # ✅ NO nested columns here
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name="ocr_output.json",
            mime="application/json"
        )

        st.download_button(
            label="📥 Download as Text",
            data=text_data,
            file_name="ocr_output.txt",
            mime="text/plain"
        )
