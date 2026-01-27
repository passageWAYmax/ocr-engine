import cv2

def draw_bounding_boxes(
    image_path: str,
    words: list,
    output_path: str,
    thickness: int = 3   # ✅ default thickness
):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    for word in words:
        x_min = word["x_min"]
        y_min = word["y_min"]
        x_max = word["x_max"]
        y_max = word["y_max"]

        cv2.rectangle(
            image,
            (x_min, y_min),
            (x_max, y_max),
            color=(255, 0, 0),   # Blue box
            thickness=thickness # ✅ now supported
        )

    cv2.imwrite(output_path, image)

    return output_path
