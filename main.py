import os
import json

from preprocessing.image_preprocess import preprocess_image
from ocr.paddle_ocr import extract_text
from postprocessing.layout_grouping import group_words


def run_ocr(image_path: str) -> dict:
    """
    End-to-end OCR pipeline using PaddleOCR
    """

    # ensure output directory
    os.makedirs("output", exist_ok=True)

    # preprocessed image path
    preprocessed_image_path = os.path.join(
        "output",
        f"preprocessed_{os.path.basename(image_path)}"
    )

    # 1️⃣ Preprocess image (OpenCV)
    clean_image_path = preprocess_image(
        image_path,
        preprocessed_image_path
    )

    # 2️⃣ OCR (PaddleOCR → word-level)
    words = extract_text(clean_image_path)

    # 3️⃣ Layout grouping (merge words → meaningful lines)
    grouped_fields = group_words(words)

    # 4️⃣ Build output JSON (client-ready)
    result = {
        "fields": {
            f"field_{i+1}": text
            for i, text in enumerate(grouped_fields)
        },
        "engine": "paddleocr",
        "total_fields": len(grouped_fields)
    }

    # 5️⃣ Save output
    output_path = os.path.join("output", "meter_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


if __name__ == "__main__":
    # for CLI testing
    run_ocr("images/sample.jpg")
