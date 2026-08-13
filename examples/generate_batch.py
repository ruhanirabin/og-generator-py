"""Generate one image per non-empty line in a UTF-8 text file."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("titles", type=Path, help="UTF-8 file with one title per line")
    parser.add_argument(
        "-d", "--output-dir", type=Path, default=Path.cwd(), help="Output directory"
    )
    parser.add_argument("--theme", default="midnight-violet")
    parser.add_argument("--logo", type=Path)
    parser.add_argument("--format", choices=("png", "webp"), default="png")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    titles = [
        line.strip()
        for line in args.titles.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for title in titles:
        command = [
            "ogimg",
            title,
            "--theme",
            args.theme,
            "--format",
            args.format,
        ]
        if args.logo is not None:
            command.extend(("--logo", str(args.logo.resolve())))
        subprocess.run(command, cwd=args.output_dir, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
