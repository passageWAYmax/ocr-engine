# postprocessing/draw_bounding_boxes.py

import cv2
import os

def draw_bounding_boxes(
    image_path: str,
    words: list,
    output_path: str
) -> str:
    """
    Draw bounding boxes on image for all OCR-detected words
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    for word in words:
        x1, y1 = word["x_min"], word["y_min"]
        x2, y2 = word["x_max"], word["y_max"]

        # Draw rectangle
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color=(0, 120, 255),  # Blue (BGR)
            thickness=4
        )

        # Optional: draw text label
        cv2.putText(
            image,
            word["text"],
            (x1, max(y1 - 5, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 120, 255),
            1,
            cv2.LINE_AA
        )

    cv2.imwrite(output_path, image)

    return output_path
