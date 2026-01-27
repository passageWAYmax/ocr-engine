import os
import google.generativeai as genai
import traceback

#  Load API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyBHOTop1YGvUA_8DAt9F3CBkBPpXw2mBw0")

MODEL_NAME = "models/gemini-3-flash-preview"


def ask_gemini(prompt: str) -> str:
    """
    Sends prompt to Gemini and returns raw text response.
    Prints full errors to terminal if anything fails.
    """

    try:
        print("\n📤 Sending prompt to Gemini...\n")

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 2048,
            }
        )

        print("\n📥 Gemini response received successfully.\n")
        print("Raw Gemini Response:\n", response.text)

        return response.text.strip()

    except Exception as e:
        print("\n❌ ERROR calling Gemini API:\n")
        traceback.print_exc()
        raise RuntimeError(f"Gemini API call failed: {e}")


# print("Available Models:")
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         # This prints the full name, e.g., models/gemini-1.5-flash
#         # But in the code, you usually strip 'models/'
#         print(f" - {m.name}")
