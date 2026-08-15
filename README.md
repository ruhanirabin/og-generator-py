# ogimg

Turn a title into a clean social image, without turning it into a whole design
project.

```sh
ogimg "OG Images Without Making It a Whole Design Flip-flop" --theme violet-bloom
```

That command creates:

```text
og-og-images-without-making-it-a-whole-design-flip-flop.png
```

No canvas setup. No nudging text boxes around. No filename debate. Just an
image ready for a post.

## The backstory

I was putting together drafts for
[One Small Fix](https://onesmallfix.substack.com/) and kept running into the
boring part nobody really wants to think about: every post wants a social image.

Making one social image is harmless; repeating the same edit, adjust, and export
routine for every post is not. So I wrote a small Python command I could drop
into my publishing workflow, run, and mostly forget about.

That is `ogimg`: small enough to maintain, predictable enough to script, and
boring enough to reuse. The longer version of the story is in
[OG Images Without Making It a Whole Design Flip-flop](https://mind.ruhanirabin.com/projects/og-images-without-making-it-a-whole-design-flip-flop).

## What it does

Give `ogimg` a title and it will:

- render it on a procedural gradient background;
- measure the actual glyphs to find a balanced, readable layout;
- add an optional transparent PNG or WebP logo;
- create a predictable filename when you do not provide one; and
- save a deterministic PNG or WebP image.

It deliberately refuses to silently cut off a title. If the text cannot fit at
the minimum readable size, the command exits with a clear error.

## Install

`ogimg` requires Python 3.10 or newer. The cleanest way to install the command
from GitHub is with [pipx](https://pipx.pypa.io/stable/installation/):

```sh
pipx install git+https://github.com/ruhanirabin/og-generator-py.git
ogimg --help
```

If you do not have pipx yet:

```sh
# Fedora
sudo dnf install pipx

# Ubuntu 23.04 or newer
sudo apt update && sudo apt install pipx

# macOS with Homebrew
brew install pipx

# Windows PowerShell, with Python already installed
py -m pip install --user pipx
```

Run `pipx ensurepath` and restart the terminal if `ogimg` is not found after
installation.

To reinstall the latest version from GitHub or remove it:

```sh
pipx reinstall ogimg
pipx uninstall ogimg
```

Check the installed version at any time:

```sh
ogimg --version
```

### Installation troubleshooting

If installation stops early, check the prerequisites first:

```sh
python --version
pipx --version
git --version
```

On Windows, use `py --version` if `python` is not recognized. `ogimg` needs
Python 3.10 or newer. Install missing software from the official
[Python downloads](https://www.python.org/downloads/) or
[Git downloads](https://git-scm.com/downloads), then follow the linked pipx
installation guide above.

If Git is unavailable, pipx can install the public GitHub source archive
instead:

```sh
pipx install https://github.com/ruhanirabin/og-generator-py/archive/refs/heads/main.zip
```

If installation succeeds but the command is missing, run `pipx ensurepath`,
close the terminal completely, and open it again. Pillow is installed
automatically with `ogimg`; users do not need to install it separately.

### Install for development

```sh
git clone https://github.com/ruhanirabin/og-generator-py.git
cd og-generator-py
python -m pip install -e '.[dev]'
```

Pillow is the only runtime dependency. The project uses Hatchling and a
`src/` package layout.

## Quick start

The title is the only required argument:

```sh
ogimg "A clean article title"
```

The image is written to the current directory as:

```text
og-a-clean-article-title.png
```

Choose the output path when you want something different. Missing parent
directories are created automatically:

```sh
ogimg "A clean article title" -o social/article.png
```

The built-in `og` preset is 1200×630, which meets Substack's documented
minimum dimensions for a
[social or post preview image](https://support.substack.com/hc/en-us/articles/4408381685268-What-are-the-optimal-image-dimensions-for-my-Substack-publication).

## All command-line options

```text
ogimg TITLE [-o PATH] [--format {png,webp}] [--preset {og}]
            [--theme THEME] [--logo PATH]
            [--logo-position {auto,top-left,top-center,top-right}]
ogimg --version
```

| Option | Default | What it does |
| --- | --- | --- |
| `TITLE` | required | The text rendered on the image. Quote titles containing spaces. |
| `-o`, `--output PATH` | derived filename | Writes to a `.png` or `.webp` path. |
| `--format {png,webp}` | `png` | Selects the format when the output path is derived or has no extension. |
| `--preset {og}` | `og` | Selects the canvas geometry. Currently `og` is 1200×630. |
| `--theme THEME` | `midnight-violet` | Selects one of the five built-in backgrounds listed below. |
| `--logo PATH` | none | Adds a transparent PNG or WebP logo. |
| `--logo-position POSITION` | `auto` | Uses `auto`, `top-left`, `top-center`, or `top-right`. |
| `-h`, `--help` | — | Shows the command help. |
| `--version` | — | Prints the installed `ogimg` version. |

Run `ogimg --help` to see the choices provided by your installed version.

## Themes

Every background is generated in code, so there are no base images to find,
crop, or ship.

| Theme | Gradient | Character |
| --- | --- | --- |
| `midnight-violet` | vertical | dark navy into vivid violet |
| `graphite-indigo` | diagonal | restrained plum-indigo into graphite |
| `deep-ocean` | horizontal | deep navy into muted teal-blue |
| `ocean-orbit` | off-center radial | muted teal glow from the upper right |
| `violet-bloom` | off-center radial | violet glow from the left |

```sh
ogimg "A clean article title" --theme midnight-violet
ogimg "A clean article title" --theme graphite-indigo
ogimg "A clean article title" --theme deep-ocean
ogimg "A clean article title" --theme ocean-orbit
ogimg "A clean article title" --theme violet-bloom
```

## Logos

Pass a transparent PNG or WebP logo with `--logo`:

```sh
ogimg "A clean article title" --logo path/to/logo.webp
```

The default `auto` placement looks at the visible part of the logo rather than
its transparent canvas. A wordmark with an aspect ratio of 2:1 or wider is
centered above the title; a compact mark goes in the top-left corner.

You can override that decision:

```sh
ogimg "A clean article title" \
  --logo path/to/logo.png \
  --logo-position top-right \
  -o social/article.png
```

Available positions are `auto`, `top-left`, `top-center`, and `top-right`.
Corner logos do not move the centered title. A centered wordmark reserves space
above it.

## Output and filenames

An explicit `.png` or `.webp` extension selects the output format:

```sh
ogimg "A clean article title" -o article.png
ogimg "A clean article title" -o article.webp
```

Without `-o`, use `--format` to change the derived extension:

```sh
ogimg "A clean article title" --format webp
# og-a-clean-article-title.webp
```

PNG is lossless and is the default. WebP uses fixed lossy settings—quality 85
and method 6—for smaller social-preview files.

Derived filenames use an `og-` prefix, lowercase ASCII letters and numbers,
and hyphens in place of whitespace or punctuation. The slug is limited to 80
characters. Latin Unicode is normalized where possible; a title with no ASCII
representation falls back to `og-image.png` (or `.webp`).

If a file already exists at the output path, it is replaced.

## Batch generation

For a list of posts, put one title on each line of a UTF-8 text file and use the
included cross-platform helper:

```sh
cp examples/titles.example.txt titles.txt
python examples/generate_batch.py titles.txt --output-dir generated

python examples/generate_batch.py titles.txt \
  --output-dir generated \
  --theme ocean-orbit \
  --format webp \
  --logo path/to/logo.webp
```

The helper supports `--output-dir`, `--theme`, `--format`, and `--logo`; it
otherwise uses the CLI defaults. Empty lines are ignored.

Duplicate titles—or different titles that sanitize to the same slug—use the
same filename, so the later image replaces the earlier one. Use explicit
output paths in your own script when both files need to be kept.

## Predictable by design

The useful part of this tool is that it does one job and gets out of the way.
Its three concerns stay separate:

```text
preset  = canvas dimensions and layout geometry
theme   = colors and visual appearance
content = title and optional logo
```

Title wrapping is based on rendered glyph measurements, not character counts.
The bundled Noto Sans Bold font is loaded from the Python package, so output
does not depend on fonts installed on the machine or the directory where the
command runs. There is no runtime dependency on ImageMagick, Node.js, browser
automation, or a POSIX shell.

Given the same title, preset, theme, logo, package version, Pillow version, and
font, PNG output is byte-for-byte repeatable. Changing one of those inputs can
change the pixels.

The implementation uses cross-platform Python APIs and is currently verified
on Linux. macOS and Windows are designed targets but still need CI verification
before being described as tested platforms.

## Development

Run the full local check suite from the project root:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m build
git diff --check
```

The root [VERSION](VERSION) file is the single source of truth for releases,
build metadata, and `ogimg --version`. User-visible changes are recorded in
[CHANGELOG.md](CHANGELOG.md), following Keep a Changelog conventions.

The core intentionally stays narrow. More presets, configuration, and
cross-platform CI are natural follow-ups; raster base images and a full design
editor are not the point of the tool.

Project guidance lives in [AGENTS.md](AGENTS.md), with durable architecture
notes in [docs/project-memory.md](docs/project-memory.md).

> **Development note:** This project has been built with assistance from AI
> tools. [AGENTS.md](AGENTS.md), project memory, tests, and dated worklogs are
> maintained so human contributors and other coding agents can understand the
> decisions already made and continue the work consistently. AI-generated
> changes are still expected to be reviewed and verified like any other
> contribution.

## License

Copyright © 2026 [Ruhani Rabin](https://www.ruhanirabin.com).

`ogimg` is released under the [MIT License](LICENSE). The bundled Noto Sans
Bold font comes from the [Noto fonts project](https://github.com/notofonts/noto-fonts)
and is redistributed under the SIL Open Font License 1.1; its license text is
included with the font.
