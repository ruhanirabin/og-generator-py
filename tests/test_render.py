from pathlib import Path

import pytest
from PIL import Image

from ogimg.render import RenderError, _load_logo, _resolve_logo_position, render_image


def test_render_is_deterministic_png(tmp_path: Path) -> None:
    first = render_image("A deterministic social image", tmp_path / "first.png")
    second = render_image("A deterministic social image", tmp_path / "second.png")

    assert first.read_bytes() == second.read_bytes()
    with Image.open(first) as image:
        assert image.format == "PNG"
        assert image.size == (1200, 630)
        assert image.mode == "RGB"


@pytest.mark.parametrize(
    ("theme", "start", "end"),
    [
        ("midnight-violet", (10, 15, 35), (91, 33, 182)),
        ("graphite-indigo", (47, 39, 78), (12, 14, 28)),
        ("deep-ocean", (4, 20, 34), (8, 52, 72)),
    ],
)
def test_theme_gradient_reaches_endpoint_colors(
    tmp_path: Path,
    theme: str,
    start: tuple[int, int, int],
    end: tuple[int, int, int],
) -> None:
    output = render_image("Theme", tmp_path / f"{theme}.png", theme_name=theme)

    with Image.open(output) as image:
        assert image.getpixel((0, 0)) == start
        assert image.getpixel((1199, 629)) == end


@pytest.mark.parametrize(
    ("theme", "center", "start", "far_corner", "end"),
    [
        (
            "ocean-orbit",
            (1079, 113),
            (14, 67, 88),
            (0, 629),
            (3, 16, 30),
        ),
        (
            "violet-bloom",
            (59, 314),
            (95, 44, 170),
            (1199, 0),
            (9, 13, 30),
        ),
    ],
)
def test_radial_theme_uses_off_center_origin(
    tmp_path: Path,
    theme: str,
    center: tuple[int, int],
    start: tuple[int, int, int],
    far_corner: tuple[int, int],
    end: tuple[int, int, int],
) -> None:
    output = render_image("Radial", tmp_path / f"{theme}.png", theme_name=theme)

    with Image.open(output) as image:
        assert image.getpixel(center) == start
        assert image.getpixel(far_corner) == end


def test_render_rejects_blank_title(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match="does not fit"):
        render_image("   ", tmp_path / "blank.png")


def test_render_rejects_non_png_output(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match=".png output only"):
        render_image("Title", tmp_path / "image.webp")


def test_render_composites_transparent_logo(tmp_path: Path) -> None:
    logo_path = tmp_path / "logo.webp"
    logo = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
    for x in range(75, 125):
        for y in range(25, 75):
            logo.putpixel((x, y), (255, 0, 0, 255))
    logo.save(logo_path, "WEBP", lossless=True)

    output = render_image("Logo test", tmp_path / "logo-test.png", logo=logo_path)

    with Image.open(output) as image:
        left_logo_area = image.crop((64, 64, 176, 176))
        red, green, _ = left_logo_area.split()
        assert red.getextrema()[1] > 200
        assert green.getextrema()[0] < 80


def test_render_rejects_missing_logo(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match="Logo file does not exist"):
        render_image("Title", tmp_path / "image.png", logo=tmp_path / "missing.png")


def test_auto_logo_position_uses_visible_aspect_ratio(tmp_path: Path) -> None:
    logo_path = tmp_path / "wide-canvas.png"
    logo = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    for x in range(100, 300):
        for y in range(175, 225):
            logo.putpixel((x, y), (255, 255, 255, 255))
    logo.save(logo_path)

    loaded = _load_logo(logo_path)

    assert loaded.size == (200, 50)
    assert _resolve_logo_position(loaded, "auto") == "top-center"

    output = render_image("Wordmark", tmp_path / "wordmark.png", logo=logo_path)
    with Image.open(output) as image:
        assert image.getpixel((600, 64)) == (255, 255, 255)


def test_explicit_top_right_logo_position(tmp_path: Path) -> None:
    logo_path = tmp_path / "logo.png"
    Image.new("RGBA", (40, 40), (255, 0, 0, 255)).save(logo_path)

    output = render_image(
        "Right logo", tmp_path / "right.png", logo=logo_path, logo_position="top-right"
    )

    with Image.open(output) as image:
        assert image.getpixel((1135, 64))[0] > 200


def test_render_rejects_invisible_logo(tmp_path: Path) -> None:
    logo_path = tmp_path / "invisible.png"
    Image.new("RGBA", (40, 40), (0, 0, 0, 0)).save(logo_path)

    with pytest.raises(RenderError, match="no visible pixels"):
        render_image("Title", tmp_path / "image.png", logo=logo_path)
