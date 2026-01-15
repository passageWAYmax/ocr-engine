def group_words(words):
    # Sort top to bottom, left to right
    words = sorted(words, key=lambda w: (w["y_min"], w["x_min"]))

    lines = []
    current_line = []

    VERTICAL_THRESHOLD = 15   # pixels

    for word in words:
        if not current_line:
            current_line.append(word)
            continue

        prev = current_line[-1]

        if abs(word["y_min"] - prev["y_min"]) <= VERTICAL_THRESHOLD:
            current_line.append(word)
        else:
            lines.append(current_line)
            current_line = [word]

    if current_line:
        lines.append(current_line)

    fields = []
    HORIZONTAL_THRESHOLD = 25  # pixels

    for line in lines:
        line = sorted(line, key=lambda w: w["x_min"])
        field = line[0]["text"]

        for i in range(1, len(line)):
            gap = line[i]["x_min"] - line[i-1]["x_max"]

            if gap <= HORIZONTAL_THRESHOLD:
                field += " " + line[i]["text"]
            else:
                fields.append(field)
                field = line[i]["text"]

        fields.append(field)

    return fields
