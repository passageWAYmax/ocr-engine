# newest working changes --------------------------------------
import os

# ---- HARD DISABLE EXPERIMENTAL BACKENDS ----
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_pir"] = "0"
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PaddleOCR


# ✅ Classic PaddleOCR (stable on Windows)
# ocr = PaddleOCR(
#     lang="en",
#     use_angle_cls=False
# )
ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False,
    show_log=False
)

def extract_text(image_path):
    """
    Returns word-level OCR output compatible with layout_grouping.py
    Uses classic PaddleOCR engine (NOT PaddleX pipeline)
    """
    result = ocr.ocr(image_path)

    words = []

    if not result:
        return words

    for line in result:
        for word_info in line:
            text = word_info[1][0]
            box = word_info[0]

            xs = [p[0] for p in box]
            ys = [p[1] for p in box]

            words.append({
                "text": text.strip(),
                "x_min": int(min(xs)),
                "y_min": int(min(ys)),
                "x_max": int(max(xs)),
                "y_max": int(max(ys))
            })

    return words

