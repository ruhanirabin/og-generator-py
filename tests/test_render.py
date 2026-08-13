from pathlib import Path

import pytest
from PIL import Image

from ogimg.render import RenderError, render_image


def test_render_is_deterministic_png(tmp_path: Path) -> None:
    first = render_image("A deterministic social image", tmp_path / "first.png")
    second = render_image("A deterministic social image", tmp_path / "second.png")

    assert first.read_bytes() == second.read_bytes()
    with Image.open(first) as image:
        assert image.format == "PNG"
        assert image.size == (1200, 630)
        assert image.mode == "RGB"


def test_render_rejects_blank_title(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match="does not fit"):
        render_image("   ", tmp_path / "blank.png")


def test_render_rejects_non_png_output(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match=".png output only"):
        render_image("Title", tmp_path / "image.webp")


def test_render_composites_transparent_logo(tmp_path: Path) -> None:
    logo_path = tmp_path / "logo.webp"
    logo = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
    for x in range(50, 150):
        for y in range(25, 75):
            logo.putpixel((x, y), (255, 0, 0, 255))
    logo.save(logo_path, "WEBP", lossless=True)

    output = render_image("Logo test", tmp_path / "logo-test.png", logo=logo_path)

    with Image.open(output) as image:
        center_column = [image.getpixel((600, y)) for y in range(105, 525)]
        assert any(red > 200 and green < 80 for red, green, _ in center_column)


def test_render_rejects_missing_logo(tmp_path: Path) -> None:
    with pytest.raises(RenderError, match="Logo file does not exist"):
        render_image("Title", tmp_path / "image.png", logo=tmp_path / "missing.png")
