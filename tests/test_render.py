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
