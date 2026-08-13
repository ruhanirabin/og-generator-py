from pathlib import Path

from PIL import Image

from ogimg.cli import main


def test_cli_generates_png(tmp_path: Path, capsys) -> None:
    output = tmp_path / "article.png"

    result = main(["A clean article title", "-o", str(output)])

    assert result == 0
    assert capsys.readouterr().out.strip() == str(output)
    with Image.open(output) as image:
        assert image.size == (1200, 630)


def test_cli_reports_overflow(tmp_path: Path, capsys) -> None:
    output = tmp_path / "overflow.png"

    result = main(["W" * 200, "-o", str(output)])

    assert result == 2
    assert "minimum readable size" in capsys.readouterr().err
    assert not output.exists()


def test_cli_accepts_logo(tmp_path: Path) -> None:
    logo = tmp_path / "logo.png"
    Image.new("RGBA", (20, 20), "white").save(logo)
    output = tmp_path / "with-logo.png"

    result = main(
        [
            "Branded image",
            "--logo",
            str(logo),
            "--logo-position",
            "top-right",
            "-o",
            str(output),
        ]
    )

    assert result == 0
    assert output.exists()
