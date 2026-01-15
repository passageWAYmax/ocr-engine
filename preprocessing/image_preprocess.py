import cv2

def preprocess_image(input_path, output_path):
    # 1️⃣ Read image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("❌ Image not found")

    # 2️⃣ Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3️⃣ Gentle noise removal (DO NOT overdo)
    denoised = cv2.fastNlMeansDenoising(
        gray,
        h=10,           # noise strength
        templateWindowSize=7,
        searchWindowSize=21
    )

    # 4️⃣ Contrast enhancement (OCR friendly)
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    contrast = clahe.apply(denoised)

    # 5️⃣ Adaptive threshold (balanced)
    processed = cv2.adaptiveThreshold(
        contrast,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,   # block size (odd)
        5     # constant
    )

    # 6️⃣ Save output
    cv2.imwrite(output_path, contrast)
    print(f"✅ Preprocessing done. Saved at: {output_path}")
    return output_path

if __name__ == "__main__":
    INPUT_IMAGE = "meter.jpg"       # your original image
    OUTPUT_IMAGE = "meter_clean.jpg"

    preprocess_image(INPUT_IMAGE, OUTPUT_IMAGE)
