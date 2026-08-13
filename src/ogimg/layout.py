from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from PIL import ImageDraw, ImageFont


@dataclass(frozen=True)
class TitleLayout:
    lines: tuple[str, ...]
    font: ImageFont.FreeTypeFont
    font_size: int
    line_widths: tuple[int, ...]
    line_height: int
    total_height: int


def _partitions(words: list[str], line_count: int):
    for breaks in combinations(range(1, len(words)), line_count - 1):
        edges = (0, *breaks, len(words))
        yield tuple(
            " ".join(words[start:end])
            for start, end in zip(edges, edges[1:], strict=False)
        )


def _measure(
    draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont
) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def fit_title(
    draw: ImageDraw.ImageDraw,
    title: str,
    font_path: str,
    max_width: int,
    max_height: int,
    max_font_size: int,
    min_font_size: int,
    max_lines: int,
    spacing: int,
) -> TitleLayout | None:
    words = title.split()
    if not words:
        return None

    for size in range(max_font_size, min_font_size - 1, -1):
        font = ImageFont.truetype(font_path, size=size)
        line_height = _measure(draw, "Ag", font)[1]
        candidates = []
        for count in range(1, min(max_lines, len(words)) + 1):
            total_height = count * line_height + (count - 1) * spacing
            if total_height > max_height:
                continue
            for lines in _partitions(words, count):
                widths = tuple(_measure(draw, line, font)[0] for line in lines)
                if max(widths) <= max_width:
                    imbalance = max(widths) - min(widths)
                    candidates.append(
                        (count, imbalance, max(widths), lines, widths, total_height)
                    )
        if candidates:
            _, _, _, lines, widths, total_height = min(candidates)
            return TitleLayout(lines, font, size, widths, line_height, total_height)
    return None
