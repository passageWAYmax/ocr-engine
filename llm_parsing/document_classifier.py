from llm_parsing.mistral_client import ask_mistral


def classify_document(ocr_text: str) -> str:
    prompt = f"""
Classify the document type from the text below.

Return ONLY one of:
- SALES_INVOICE
- WARRANTY_CLAIM
- OTHER

TEXT:
{ocr_text}
"""
    response = ask_mistral(prompt)
    return response.strip().upper()
