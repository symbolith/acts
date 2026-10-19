import sys
import unicodedata

MAXIMUM_WIDTH = 98


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(character) in "WF" else 1 for character in text)


def split_row(line):
    cells = []
    current = []
    escaped = False
    for character in line.strip().strip("|"):
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            current.append(character)
            escaped = True
        elif character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    cells.append("".join(current).strip())
    return cells


def is_separator(cells):
    return all(cell and set(cell) <= set(":-") for cell in cells)


def alignment(cell):
    left = cell.startswith(":")
    right = cell.endswith(":")
    if left and right:
        return "center"
    if right:
        return "right"
    return "left"


def pad(cell, width, align):
    gap = width - display_width(cell)
    if align == "right":
        return " " * gap + cell
    if align == "center":
        return " " * (gap // 2) + cell + " " * (gap - gap // 2)
    return cell + " " * gap


def separator(width, align):
    if align == "center":
        return ":" + "-" * (width - 2) + ":"
    if align == "right":
        return "-" * (width - 1) + ":"
    return "-" * width


def align_table(lines):
    rows = [split_row(line) for line in lines if line.strip()]
    if len(rows) < 2 or not is_separator(rows[1]):
        sys.exit("expected a header row followed by a separator row")
    column_count = max(len(row) for row in rows)
    rows = [row + [""] * (column_count - len(row)) for row in rows]
    alignments = [alignment(cell) for cell in rows[1]]
    body = [row for index, row in enumerate(rows) if index != 1]
    widths = [
        max(3, max(display_width(row[column]) for row in body))
        for column in range(column_count)
    ]
    output = []
    for index, row in enumerate(rows):
        if index == 1:
            cells = [separator(widths[column], alignments[column]) for column in range(column_count)]
        else:
            cells = [pad(row[column], widths[column], alignments[column]) for column in range(column_count)]
        output.append("| " + " | ".join(cells) + " |")
    return output


def main():
    output = align_table(sys.stdin.read().splitlines())
    print("\n".join(output))
    widest = max(display_width(line) for line in output)
    if widest > MAXIMUM_WIDTH:
        print(f"row width {widest} exceeds {MAXIMUM_WIDTH}: shorten cells or drop a column", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
