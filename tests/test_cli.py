"""CLI tests; the project version is defined in the root VERSION file."""

from pathlib import Path

import pytest
from PIL import Image

from ogimg.cli import default_output_path, main


def test_cli_reports_package_version(capsys) -> None:
    from ogimg import __version__

    with pytest.raises(SystemExit, match="0"):
        main(["--version"])

    assert capsys.readouterr().out.strip() == f"ogimg {__version__}"


def test_cli_generates_png(tmp_path: Path, capsys) -> None:
    output = tmp_path / "article.png"

    result = main(["A clean article title", "-o", str(output)])

    assert result == 0
    assert capsys.readouterr().out.strip() == str(output)
    with Image.open(output) as image:
        assert image.size == (1200, 630)


def test_cli_derives_output_from_title(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["Fix Proxmox: High CPU Temperature!"])

    output = tmp_path / "og-fix-proxmox-high-cpu-temperature.png"
    assert result == 0
    assert capsys.readouterr().out.strip() == output.name
    assert output.exists()


def test_default_output_path_normalizes_and_limits_title() -> None:
    output = default_output_path("  Déjà Vu — " + "Long " * 30)

    assert output.suffix == ".png"
    assert output.name.startswith("og-deja-vu-long-long")
    assert len(output.stem.removeprefix("og-")) <= 80


def test_default_output_path_falls_back_for_non_ascii_title() -> None:
    assert default_output_path("你好世界") == Path("og-image.png")


def test_cli_derives_webp_output_from_format(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["Social preview", "--format", "webp"])

    output = tmp_path / "og-social-preview.webp"
    assert result == 0
    with Image.open(output) as image:
        assert image.format == "WEBP"
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
