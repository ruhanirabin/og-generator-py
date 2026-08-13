from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path

from PIL import Image, ImageDraw

from ogimg.layout import fit_title
from ogimg.models import Preset, Theme
from ogimg.templates import PRESETS, THEMES


class RenderError(ValueError):
    """Raised when supplied content cannot be rendered safely."""


def _gradient(preset: Preset, theme: Theme) -> Image.Image:
    image = Image.new("RGB", (preset.width, preset.height))
    pixels = image.load()
    denominator = max(preset.height - 1, 1)
    for y in range(preset.height):
        color = tuple(
            start + ((end - start) * y // denominator)
            for start, end in zip(theme.gradient_start, theme.gradient_end, strict=True)
        )
        for x in range(preset.width):
            pixels[x, y] = color
    return image


def _load_logo(logo_path: Path) -> Image.Image:
    try:
        with Image.open(logo_path) as source:
            logo = source.convert("RGBA")
    except FileNotFoundError as error:
        raise RenderError(f"Logo file does not exist: {logo_path}") from error
    except Image.UnidentifiedImageError as error:
        raise RenderError(f"Logo is not a supported image: {logo_path}") from error

    logo.thumbnail((112, 112), Image.Resampling.LANCZOS)
    return logo


def render_image(
    title: str,
    output: str | Path,
    *,
    preset_name: str = "og",
    theme_name: str = "midnight-violet",
    logo: str | Path | None = None,
) -> Path:
    try:
        preset = PRESETS[preset_name]
    except KeyError as error:
        raise RenderError(f"Unknown preset: {preset_name}") from error
    try:
        theme = THEMES[theme_name]
    except KeyError as error:
        raise RenderError(f"Unknown theme: {theme_name}") from error

    output_path = Path(output)
    if output_path.suffix.lower() != ".png":
        raise RenderError("The first implementation supports .png output only")

    image = _gradient(preset, theme)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = preset.text_box
    logo_image = _load_logo(Path(logo)) if logo is not None else None
    logo_gap = 36 if logo_image is not None else 0
    logo_height = logo_image.height if logo_image is not None else 0
    available_text_height = bottom - top - logo_height - logo_gap
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
        logo_x = (preset.width - logo_image.width) // 2
        image.paste(logo_image, (logo_x, logo_y), logo_image)
        y = logo_y + logo_height + logo_gap
    else:
        y = top + ((bottom - top - layout.total_height) // 2)
    for line, width in zip(layout.lines, layout.line_widths, strict=True):
        x = left + ((right - left - width) // 2)
        draw.text((x, y), line, font=layout.font, fill=theme.text_color)
        y += layout.line_height + theme.line_spacing

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=False, compress_level=9)
    return output_path
