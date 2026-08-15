"""Deterministic image renderer; the project version is defined in root VERSION."""

from __future__ import annotations

from importlib.resources import as_file, files
from math import isqrt
from pathlib import Path

from PIL import Image, ImageDraw

from ogimg.layout import fit_title
from ogimg.models import Preset, Theme
from ogimg.templates import PRESETS, THEMES

LOGO_POSITIONS = ("auto", "top-left", "top-center", "top-right")
OUTPUT_FORMATS = ("png", "webp")


class RenderError(ValueError):
    """Raised when supplied content cannot be rendered safely."""


def _resolve_output(output: str | Path, output_format: str | None) -> tuple[Path, str]:
    output_path = Path(output)
    suffix_format = output_path.suffix.lower().removeprefix(".")
    if output_format is not None and output_format not in OUTPUT_FORMATS:
        raise RenderError(f"Unsupported output format: {output_format}")
    if suffix_format and suffix_format not in OUTPUT_FORMATS:
        raise RenderError("Output must use a .png or .webp extension")
    if output_format is not None:
        if suffix_format and suffix_format != output_format:
            raise RenderError(
                f"Output extension .{suffix_format} conflicts with "
                f"format {output_format}"
            )
        if not suffix_format:
            output_path = output_path.with_suffix(f".{output_format}")
        return output_path, output_format
    if not suffix_format:
        raise RenderError("Output must use a .png or .webp extension")
    return output_path, suffix_format


def _gradient(preset: Preset, theme: Theme) -> Image.Image:
    image = Image.new("RGB", (preset.width, preset.height))
    pixels = image.load()
    if theme.gradient_kind == "linear":
        horizontal, vertical = theme.gradient_direction
        denominator = max(
            (preset.width - 1) * horizontal + (preset.height - 1) * vertical, 1
        )

        def progress_at(x: int, y: int) -> int:
            return x * horizontal + y * vertical

    elif theme.gradient_kind == "radial" and theme.gradient_center is not None:
        center_x = (preset.width - 1) * theme.gradient_center[0] // 1000
        center_y = (preset.height - 1) * theme.gradient_center[1] // 1000
        corner_distances = (
            center_x**2 + center_y**2,
            (preset.width - 1 - center_x) ** 2 + center_y**2,
            center_x**2 + (preset.height - 1 - center_y) ** 2,
            (preset.width - 1 - center_x) ** 2 + (preset.height - 1 - center_y) ** 2,
        )
        denominator = max(isqrt(max(corner_distances)), 1)

        def progress_at(x: int, y: int) -> int:
            return min(isqrt((x - center_x) ** 2 + (y - center_y) ** 2), denominator)

    else:
        raise RenderError(f"Unsupported gradient kind: {theme.gradient_kind}")

    for y in range(preset.height):
        for x in range(preset.width):
            progress = progress_at(x, y)
            pixels[x, y] = tuple(
                start + ((end - start) * progress // denominator)
                for start, end in zip(
                    theme.gradient_start, theme.gradient_end, strict=True
                )
            )
    return image


def _load_logo(logo_path: Path) -> Image.Image:
    try:
        with Image.open(logo_path) as source:
            logo = source.convert("RGBA")
    except FileNotFoundError as error:
        raise RenderError(f"Logo file does not exist: {logo_path}") from error
    except Image.UnidentifiedImageError as error:
        raise RenderError(f"Logo is not a supported image: {logo_path}") from error

    visible_bounds = logo.getchannel("A").getbbox()
    if visible_bounds is None:
        raise RenderError(f"Logo has no visible pixels: {logo_path}")
    return logo.crop(visible_bounds)


def _resolve_logo_position(logo: Image.Image, position: str) -> str:
    if position not in LOGO_POSITIONS:
        raise RenderError(f"Unknown logo position: {position}")
    if position != "auto":
        return position
    return "top-center" if logo.width / logo.height >= 2 else "top-left"


def _size_logo(logo: Image.Image, position: str) -> Image.Image:
    max_size = (280, 80) if position == "top-center" else (112, 112)
    logo.thumbnail(max_size, Image.Resampling.LANCZOS)
    return logo


def render_image(
    title: str,
    output: str | Path,
    *,
    preset_name: str = "og",
    theme_name: str = "midnight-violet",
    logo: str | Path | None = None,
    logo_position: str = "auto",
    output_format: str | None = None,
) -> Path:
    try:
        preset = PRESETS[preset_name]
    except KeyError as error:
        raise RenderError(f"Unknown preset: {preset_name}") from error
    try:
        theme = THEMES[theme_name]
    except KeyError as error:
        raise RenderError(f"Unknown theme: {theme_name}") from error

    output_path, resolved_format = _resolve_output(output, output_format)

    image = _gradient(preset, theme)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = preset.text_box
    logo_image = _load_logo(Path(logo)) if logo is not None else None
    resolved_logo_position = (
        _resolve_logo_position(logo_image, logo_position)
        if logo_image is not None
        else None
    )
    if logo_image is not None and resolved_logo_position is not None:
        logo_image = _size_logo(logo_image, resolved_logo_position)
    logo_gap = 36 if logo_image is not None else 0
    logo_height = logo_image.height if logo_image is not None else 0
    available_text_height = bottom - top
    if resolved_logo_position == "top-center":
        available_text_height -= logo_height + logo_gap
    font_resource = files("ogimg.templates").joinpath("fonts/NotoSans.ttf")
    with as_file(font_resource) as font_path:
        layout = fit_title(
            draw,
            title,
            str(font_path),
            right - left,
            available_text_height,
            preset.max_font_size,
            preset.min_font_size,
            preset.max_lines,
            theme.line_spacing,
        )
    if layout is None:
        raise RenderError(
            f"Title does not fit the {preset.name!r} preset at the minimum "
            f"readable size ({preset.min_font_size}px)"
        )

    if logo_image is not None:
        logo_y = 64
        if resolved_logo_position == "top-left":
            logo_x = 64
        elif resolved_logo_position == "top-right":
            logo_x = preset.width - 64 - logo_image.width
        else:
            logo_x = (preset.width - logo_image.width) // 2
        image.paste(logo_image, (logo_x, logo_y), logo_image)
        if resolved_logo_position == "top-center":
            y = logo_y + logo_height + logo_gap
        else:
            y = top + ((bottom - top - layout.total_height) // 2)
    else:
        y = top + ((bottom - top - layout.total_height) // 2)
    for line, width in zip(layout.lines, layout.line_widths, strict=True):
        x = left + ((right - left - width) // 2)
        draw.text((x, y), line, font=layout.font, fill=theme.text_color)
        y += layout.line_height + theme.line_spacing

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if resolved_format == "png":
        image.save(output_path, format="PNG", optimize=False, compress_level=9)
    else:
        image.save(output_path, format="WEBP", lossless=False, quality=85, method=6)
    return output_path
