import os
import json

from preprocessing.image_preprocess import preprocess_image
from ocr.paddle_ocr import extract_text
from postprocessing.layout_grouping import group_words
from postprocessing.draw_bounding_boxes import draw_bounding_boxes

from llm_parsing.mistral_client import ask_mistral
from llm_parsing.gemini_client import ask_gemini

from llm_parsing.json_utils import extract_json_from_text
from llm_parsing.invoice_prompts import INVOICE_EXTRACTION_PROMPT


def run_ocr(image_path: str) -> dict:
    """
    End-to-end OCR + LLM document understanding pipeline
    """

    os.makedirs("output", exist_ok=True)

    # ---------- 1️⃣ Preprocess ----------
    preprocessed_image_path = os.path.join(
        "output", f"preprocessed_{os.path.basename(image_path)}"
    )

    clean_image_path = preprocess_image(image_path, preprocessed_image_path)

    # ---------- 2️⃣ OCR ----------
    words = extract_text(clean_image_path)

    # ---------- 3️⃣ Bounding boxes ----------
    boxed_image_path = os.path.join(
        "output", f"boxed_{os.path.basename(image_path)}"
    )

    draw_bounding_boxes(
        image_path=clean_image_path,
        words=words,
        output_path=boxed_image_path,
        thickness=3
    )

    # ---------- 4️⃣ Group OCR ----------
    grouped_fields = group_words(words)
    ocr_text = "\n".join(grouped_fields)

    # ---------- 5️⃣ LLM Parsing ----------
    prompt = INVOICE_EXTRACTION_PROMPT.format(ocr_text=ocr_text)

    print("llm_prompt_______",prompt)

    llm_response = ask_mistral(prompt)
    # llm_response = ask_gemini(prompt)

    print("llm_response_______",llm_response)

    try:
        parsed_json = extract_json_from_text(llm_response)
        print("llm_response_after parsing______",parsed_json)
    except Exception:
        parsed_json = {
            "document_type": "unknown",
            "confidence": 0.0,
            "fields": {},
            "missing_fields": ["LLM_failed_to_return_JSON"]
        }

    # ---------- 6️⃣ Final Output ----------
    result = {
        "engine": "paddleocr + mistral",
        "boxed_image_path": boxed_image_path,
        "ocr_text": grouped_fields,
        "llm_output": parsed_json
    }

    with open("output/output_document.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


if __name__ == "__main__":
    run_ocr("images/sample_document.jpg")
