#!/usr/bin/env python3

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1440
CENTER_BAND_WIDTH = 540
OUTER_CONTENT_WIDTH = 972
MAX_CONTENT_HEIGHT = 1152
ITEM_GAP = 18


def clamp(value, low, high):
    return min(max(value, low), high)


def normalize_rect(rect, image_width, image_height):
    if not isinstance(rect, list) or len(rect) != 4:
        raise ValueError(f"Expected [x, y, width, height], got {rect!r}")

    x, y, width, height = [int(round(value)) for value in rect]
    if width <= 0 or height <= 0:
        raise ValueError(f"Rectangle must have positive dimensions: {rect!r}")

    left = clamp(x, 0, image_width - 1)
    top = clamp(y, 0, image_height - 1)
    right = clamp(x + width, left + 1, image_width)
    bottom = clamp(y + height, top + 1, image_height)
    return left, top, right, bottom


def load_source(spec):
    path = Path(spec["path"]).expanduser()
    if not path.is_absolute():
        raise ValueError(f"Source path must be absolute: {path}")
    if not path.exists():
        raise FileNotFoundError(path)

    image = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    draw = ImageDraw.Draw(image)
    for mask in spec.get("masks", []):
        left, top, right, bottom = normalize_rect(mask, image.width, image.height)
        radius = max(2, min(12, (bottom - top) // 5))
        draw.rounded_rectangle((left, top, right, bottom), radius=radius, fill=(0, 0, 0))

    crop = spec.get("crop")
    if crop is not None:
        image = image.crop(normalize_rect(crop, image.width, image.height))

    return image


def center_placements(placements):
    left = min(item["x"] for item in placements)
    top = min(item["y"] for item in placements)
    right = max(item["x"] + item["width"] for item in placements)
    bottom = max(item["y"] + item["height"] for item in placements)
    offset_x = (OUTPUT_WIDTH - (right - left)) / 2 - left
    offset_y = (OUTPUT_HEIGHT - (bottom - top)) / 2 - top

    centered = []
    for item in placements:
        centered.append(
            {
                **item,
                "x": int(round(item["x"] + offset_x)),
                "y": int(round(item["y"] + offset_y)),
                "width": int(round(item["width"])),
                "height": int(round(item["height"])),
            }
        )
    return centered


def build_stack(images):
    natural_heights = [
        image.height / image.width * CENTER_BAND_WIDTH for image in images
    ]
    natural_total = sum(natural_heights) + ITEM_GAP * (len(images) - 1)
    scale = min(1.0, MAX_CONTENT_HEIGHT / natural_total)
    width = CENTER_BAND_WIDTH * scale
    gap = ITEM_GAP * scale
    placements = []
    y = 0.0

    for index, height in enumerate(natural_heights):
        scaled_height = height * scale
        placements.append(
            {
                "source_index": index,
                "x": 0.0,
                "y": y,
                "width": width,
                "height": scaled_height,
            }
        )
        y += scaled_height + gap

    return {"name": "stack", "placements": center_placements(placements)}


def build_row(images):
    gap = ITEM_GAP
    cell_width = (OUTER_CONTENT_WIDTH - gap * (len(images) - 1)) / len(images)
    sizes = []
    for index, image in enumerate(images):
        scale = min(cell_width / image.width, MAX_CONTENT_HEIGHT / image.height)
        sizes.append(
            {
                "source_index": index,
                "width": image.width * scale,
                "height": image.height * scale,
            }
        )

    max_height = max(item["height"] for item in sizes)
    placements = []
    x = 0.0

    for item in sizes:
        placements.append(
            {
                "source_index": item["source_index"],
                "x": x,
                "y": (max_height - item["height"]) / 2,
                "width": item["width"],
                "height": item["height"],
            }
        )
        x += item["width"] + gap

    return {"name": "row", "placements": center_placements(placements)}


def build_grid(images):
    columns = min(2, len(images))
    rows = math.ceil(len(images) / columns)
    cell_width = (OUTER_CONTENT_WIDTH - ITEM_GAP * (columns - 1)) / columns
    base = []

    for index, image in enumerate(images):
        scale = cell_width / image.width
        base.append(
            {
                "source_index": index,
                "width": cell_width,
                "height": image.height * scale,
            }
        )

    row_heights = []
    for row in range(rows):
        row_items = base[row * columns : row * columns + columns]
        row_heights.append(max(item["height"] for item in row_items))

    raw_height = sum(row_heights) + ITEM_GAP * (rows - 1)
    scale = min(1.0, MAX_CONTENT_HEIGHT / raw_height)
    placements = []
    y = 0.0

    for row in range(rows):
        row_items = base[row * columns : row * columns + columns]
        scaled_gap = ITEM_GAP * scale
        row_width = (
            sum(item["width"] * scale for item in row_items)
            + scaled_gap * (len(row_items) - 1)
        )
        x = (OUTER_CONTENT_WIDTH * scale - row_width) / 2

        for item in row_items:
            placements.append(
                {
                    "source_index": item["source_index"],
                    "x": x,
                    "y": y + (row_heights[row] - item["height"]) * scale / 2,
                    "width": item["width"] * scale,
                    "height": item["height"] * scale,
                }
            )
            x += item["width"] * scale + scaled_gap
        y += row_heights[row] * scale + scaled_gap

    return {"name": "grid", "placements": center_placements(placements)}


def minimum_width(layout):
    return min(item["width"] for item in layout["placements"])


def choose_layout(images, requested):
    if len(images) == 1 or requested == "stack":
        return build_stack(images)
    if requested == "row":
        return build_row(images)
    if requested == "grid":
        return build_grid(images)
    if requested != "auto":
        raise ValueError(f"Unknown layout: {requested}")

    stack = build_stack(images)
    row = build_row(images)
    candidates = [stack, row]
    if len(images) > 2:
        candidates.append(build_grid(images))

    best_width = max(minimum_width(candidate) for candidate in candidates)
    if minimum_width(stack) >= min(430, best_width * 0.92):
        return stack

    priority = {"grid": 0, "row": 1, "stack": 2}
    near_best = [
        candidate
        for candidate in candidates
        if minimum_width(candidate) >= best_width * 0.98
    ]
    return sorted(near_best, key=lambda candidate: priority[candidate["name"]])[0]


def draw_background(show_grid):
    canvas = Image.new("RGB", (OUTPUT_WIDTH, OUTPUT_HEIGHT), (0, 0, 0))
    if not show_grid:
        return canvas

    draw = ImageDraw.Draw(canvas)
    for x in (270, 540, 810):
        color = (184, 184, 184) if x == 540 else (108, 108, 108)
        width = 3 if x == 540 else 2
        draw.line((x, 0, x, OUTPUT_HEIGHT), fill=color, width=width)
    for y in (360, 720, 1080):
        color = (184, 184, 184) if y == 720 else (108, 108, 108)
        width = 3 if y == 720 else 2
        draw.line((0, y, OUTPUT_WIDTH, y), fill=color, width=width)
    return canvas


def compose_output(output, show_grid, output_dir):
    sources = output.get("sources", [])
    if not sources:
        raise ValueError("Each output requires at least one source")

    images = [load_source(source) for source in sources]
    layout = choose_layout(images, output.get("layout", "auto"))
    canvas = draw_background(show_grid)

    for placement in layout["placements"]:
        image = images[placement["source_index"]]
        width = max(1, placement["width"])
        height = max(1, placement["height"])
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        canvas.paste(resized, (placement["x"], placement["y"]))

    name = output["name"]
    if Path(name).suffix.lower() not in {".jpg", ".jpeg"}:
        name += ".jpg"
    destination = output_dir / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, "JPEG", quality=95, subsampling=0, optimize=True)

    left = min(item["x"] for item in layout["placements"])
    top = min(item["y"] for item in layout["placements"])
    right = max(item["x"] + item["width"] for item in layout["placements"])
    bottom = max(item["y"] + item["height"] for item in layout["placements"])
    center = ((left + right) / 2, (top + bottom) / 2)
    return destination, layout["name"], center


def main():
    parser = argparse.ArgumentParser(
        description="Compose centered 1080x1440 screenshot cards from a JSON manifest."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    show_grid = bool(manifest.get("show_grid", True))

    for output in manifest.get("outputs", []):
        destination, layout, center = compose_output(
            output, show_grid, output_dir
        )
        print(
            f"{destination} | layout={layout} | "
            f"center=({center[0]:.1f},{center[1]:.1f})"
        )


if __name__ == "__main__":
    main()
