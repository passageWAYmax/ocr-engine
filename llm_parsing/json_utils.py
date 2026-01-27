import json
import re


def extract_json_from_text(text: str) -> dict:
    """
    Extract the first valid JSON object from LLM output.
    """

    # 1️⃣ Try direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2️⃣ Extract {...} block
    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_str = match.group(0)

    return json.loads(json_str)
