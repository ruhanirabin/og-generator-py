"""Title-layout tests; the project version is defined in root VERSION."""

from importlib.resources import as_file, files

from PIL import Image, ImageDraw

from ogimg.layout import fit_title


def test_fit_title_balances_measured_lines() -> None:
    draw = ImageDraw.Draw(Image.new("RGB", (1200, 630)))
    resource = files("ogimg.templates").joinpath("fonts/NotoSans.ttf")
    with as_file(resource) as font_path:
        layout = fit_title(
            draw,
            "Measured words make balanced title lines",
            str(font_path),
            700,
            300,
            72,
            40,
            3,
            12,
        )

    assert layout is not None
    assert " ".join(layout.lines) == "Measured words make balanced title lines"
    assert max(layout.line_widths) <= 700
    assert layout.total_height <= 300


def test_fit_title_rejects_unbreakable_overflow() -> None:
    draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
    resource = files("ogimg.templates").joinpath("fonts/NotoSans.ttf")
    with as_file(resource) as font_path:
        layout = fit_title(draw, "W" * 100, str(font_path), 100, 100, 48, 40, 2, 10)

    assert layout is None
