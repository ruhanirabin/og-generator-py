# ogimg

`ogimg` is a small, deterministic command-line utility for generating clean,
template-based Open Graph images from a title and a procedural background.

The current vertical slice includes one 1200×630 `og` preset, five procedural
gradient themes, measured title wrapping and fitting, optional adaptive logo
placement, clear overflow errors, and PNG output.

## Install

`ogimg` requires Python 3.10 or newer. Install
[pipx](https://pipx.pypa.io/stable/installation/) before installing the CLI:

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

Then add the pipx application directory to `PATH` and restart the terminal:

```sh
pipx ensurepath
```

The repository is currently private. A GitHub user with repository access and
a configured SSH key can install it into an isolated environment:

```sh
pipx install git+ssh://git@github.com/ruhanirabin/og-generator-py.git
ogimg "A clean article title" -o article.png
```

Run `pipx ensurepath` and restart the terminal if the `ogimg` command is not
found after installation. Public installation instructions will be added when
the repository or a packaged release becomes public.

Verify, update, or remove the installation:

```sh
ogimg --help
pipx list
pipx reinstall ogimg
pipx uninstall ogimg
```

`pipx reinstall ogimg` installs the latest commit available from the configured
Git source, so repository changes must be pushed first.

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

Relative output paths are created in the current directory. For example,
running the command above from `~/Downloads` creates
`~/Downloads/article.png`. Parent directories are created automatically:

```sh
ogimg "A clean article title" -o social/article.png
```

The built-in `og` preset is 1200×630. This is the standard Open Graph canvas
used by the project and meets Substack's recommended minimum dimensions for a
[social or post preview image](https://support.substack.com/hc/en-us/articles/4408381685268-What-are-the-optimal-image-dimensions-for-my-Substack-publication).

The currently available choices are explicit in the command help:

```sh
ogimg --help
ogimg "A clean article title" --preset og --theme midnight-violet -o article.png
```

Choose one of the built-in procedural themes:

| Theme | Direction | Character |
| --- | --- | --- |
| `midnight-violet` | vertical | dark navy into vivid violet |
| `graphite-indigo` | diagonal | restrained plum-indigo into graphite |
| `deep-ocean` | horizontal | deep navy into muted teal-blue |
| `ocean-orbit` | off-center radial | muted teal glow from the upper right |
| `violet-bloom` | off-center radial | violet glow from the left |

```sh
ogimg "A clean article title" --theme graphite-indigo -o graphite.png
ogimg "A clean article title" --theme deep-ocean -o ocean.png
ogimg "A clean article title" --theme ocean-orbit -o orbit.png
ogimg "A clean article title" --theme violet-bloom -o bloom.png
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

Balanced wrapping refinements, more presets, WebP, configuration, and
cross-platform CI are planned follow-up phases. Raster base images are outside
the core template model.

Project and contributor guidance lives in [AGENTS.md](AGENTS.md). Durable
architecture context lives in [docs/project-memory.md](docs/project-memory.md).
The source repository is
[ruhanirabin/og-generator-py](https://github.com/ruhanirabin/og-generator-py)
and is private during early development.

## License

Copyright © 2026 [Ruhani Rabin](https://www.ruhanirabin.com). The project is
released under the [MIT License](LICENSE). This is separate from the bundled
font's SIL Open Font License 1.1.
