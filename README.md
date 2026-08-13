# ogimg

`ogimg` is a small, deterministic command-line utility for generating clean,
template-based Open Graph images from a title and a procedural background.

The current vertical slice includes one 1200×630 `og` preset, one
`midnight-violet` gradient theme, measured title wrapping and fitting, clear
overflow errors, and PNG output.

## Install for development

`ogimg` requires Python 3.10 or newer. From the repository root:

```sh
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

## License

Copyright © 2026 [Ruhani Rabin](https://www.ruhanirabin.com). The project is
released under the [MIT License](LICENSE). This is separate from the bundled
font's SIL Open Font License 1.1.
