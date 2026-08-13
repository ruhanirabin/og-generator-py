from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ogimg.render import RenderError, render_image
from ogimg.templates import PRESETS, THEMES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ogimg", description="Generate a deterministic social image from a title."
    )
    parser.add_argument("title", help="Title to render")
    parser.add_argument(
        "-o", "--output", required=True, type=Path, help="Output PNG path"
    )
    parser.add_argument("--preset", choices=PRESETS, default="og")
    parser.add_argument("--theme", choices=THEMES, default="midnight-violet")
    parser.add_argument(
        "--logo",
        type=Path,
        help="Optional PNG or WebP logo, centered above the title",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        output = render_image(
            args.title,
            args.output,
            preset_name=args.preset,
            theme_name=args.theme,
            logo=args.logo,
        )
    except (RenderError, OSError) as error:
        print(f"ogimg: error: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0
