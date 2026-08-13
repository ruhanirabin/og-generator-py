from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    name: str
    width: int
    height: int
    text_box: tuple[int, int, int, int]
    max_font_size: int
    min_font_size: int
    max_lines: int


@dataclass(frozen=True)
class Theme:
    name: str
    gradient_start: tuple[int, int, int]
    gradient_end: tuple[int, int, int]
    text_color: tuple[int, int, int]
    line_spacing: int
