# ogimg

`ogimg` is a small, deterministic command-line utility for generating clean,
template-based Open Graph images from a title and a procedural background.

The current vertical slice includes one 1200×630 `og` preset, one
`midnight-violet` gradient theme, measured title wrapping and fitting, clear
overflow errors, and PNG output.

## Install

The repository is currently private. GitHub users with access and a configured
SSH key can install the CLI in an isolated environment with
[pipx](https://pipx.pypa.io/):

```sh
pipx install git+ssh://git@github.com/ruhanirabin/og-generator-py.git
ogimg "A clean article title" -o article.png
```

Run `pipx ensurepath` and restart the terminal if the `ogimg` command is not
found after installation. Public installation instructions will be added when
the repository or a packaged release becomes public.

## Install for development

`ogimg` requires Python 3.10 or newer. From the repository root:

```sh
git clone git@github.com:ruhanirabin/og-generator-py.git
cd og-generator-py
python -m pip install -e '.[dev]'
```

The only runtime dependency is Pillow. The build uses Hatchling and the package
uses a `src/` layout.

## Usage

```sh
ogimg "A clean article title" -o article.png
```

The currently available choices are explicit in the command help:

```sh
ogimg --help
ogimg "A clean article title" --preset og --theme midnight-violet -o article.png
```

Add an optional transparent PNG or WebP logo. In `auto` mode, compact logos are
placed at the top left and wide wordmarks are centered above the title:

```sh
ogimg "A clean article title" --logo path/to/logo.webp -o article.png
```

Override the inferred placement when needed:

```sh
ogimg "A clean article title" \
  --logo path/to/logo.webp \
  --logo-position top-right \
  -o article.png
```

Available positions are `auto`, `top-left`, `top-center`, and `top-right`.
Automatic placement uses the logo's visible, non-transparent bounds: aspect
ratios of 2:1 or wider use `top-center`, while compact logos use `top-left`.
Corner logos do not displace the centered title; centered wordmarks reserve
vertical space above it.

The output directory is created when necessary. Titles are wrapped using
rendered glyph measurements at every candidate font size. If a title cannot fit
at the minimum readable size, the command exits with an error instead of
truncating it.

The same content, preset, theme, package version, Pillow version, and bundled
font produce the same PNG bytes. Exact pixels may change when one of those
inputs changes.

## Design

The main concepts remain independent:

```text
preset  = dimensions and layout geometry
theme   = visual appearance
content = title
```

Built-in resources are loaded through Python's package resource APIs, so the
command does not rely on the current directory or host-installed fonts. It has
no runtime dependency on ImageMagick, Node.js, browser automation, or a POSIX
shell.

The bundled Noto Sans Bold font comes from the
[Noto fonts repository](https://github.com/notofonts/noto-fonts) and is
redistributed under the SIL Open Font License 1.1; its license text is included
beside the font.

## Test and build

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m build
```

The implementation is designed around cross-platform Python APIs. Linux is the
only locally verified platform so far; macOS and Windows support must be
verified in CI before it is advertised as tested.

## Scope

Balanced wrapping refinements, more presets and themes, optional logos, WebP,
configuration, and cross-platform CI are planned follow-up phases. Raster base
images are outside the core template model.

Project and contributor guidance lives in [AGENTS.md](AGENTS.md). Durable
architecture context lives in [docs/project-memory.md](docs/project-memory.md).
The source repository is
[ruhanirabin/og-generator-py](https://github.com/ruhanirabin/og-generator-py)
and is private during early development.

## License

Copyright © 2026 [Ruhani Rabin](https://www.ruhanirabin.com). The project is
released under the [MIT License](LICENSE). This is separate from the bundled
font's SIL Open Font License 1.1.
