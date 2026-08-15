"""Command-line interface; the project version is defined in root VERSION."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections.abc import Sequence
from pathlib import Path

from ogimg import __version__
from ogimg.render import LOGO_POSITIONS, OUTPUT_FORMATS, RenderError, render_image
from ogimg.templates import PRESETS, THEMES

_NON_SLUG_CHARACTERS = re.compile(r"[^a-z0-9]+")


def default_output_path(title: str, output_format: str = "png") -> Path:
    normalized = unicodedata.normalize("NFKD", title.casefold())
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = _NON_SLUG_CHARACTERS.sub("-", ascii_title).strip("-")[:80].rstrip("-")
    return Path(f"og-{slug or 'image'}.{output_format}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ogimg", description="Generate a deterministic social image from a title."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("title", help="Title to render")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .png or .webp path (default: og-<sanitized-title>.png)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=OUTPUT_FORMATS,
        help="Output format; inferred from -o, or png by default",
    )
    parser.add_argument("--preset", choices=PRESETS, default="og")
    parser.add_argument("--theme", choices=THEMES, default="midnight-violet")
    parser.add_argument(
        "--logo",
        type=Path,
        help="Optional PNG or WebP logo",
    )
    parser.add_argument(
        "--logo-position",
        choices=LOGO_POSITIONS,
        default="auto",
        help=(
            "Logo placement; auto centers wide wordmarks and left-aligns compact logos"
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_path = args.output or default_output_path(
        args.title, args.output_format or "png"
    )
    try:
        output = render_image(
            args.title,
            output_path,
            preset_name=args.preset,
            theme_name=args.theme,
            logo=args.logo,
            logo_position=args.logo_position,
            output_format=args.output_format,
        )
    except (RenderError, OSError) as error:
        print(f"ogimg: error: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0
