# Project memory

## Goal

Create a small open-source CLI that produces polished Open Graph and article
hero images from text, procedural visual themes, and optional brand assets.

## Current baseline

- The first end-to-end vertical slice was implemented on 2026-08-13.
- It provides an installable `ogimg` command, one `og` preset, one
  `midnight-violet` procedural theme, measured balanced title fitting, clear
  overflow errors, and deterministic PNG output.
- The primary development environment is Linux. The implementation is designed
  for Linux, macOS, and Windows, but only Linux has been verified so far.
- Logo compositing, WebP output, configuration, additional presets and themes,
  and release automation remain future phases.

## Durable decisions

- Use Python and Pillow for the first implementation.
- Keep the renderer deterministic and local; AI is not part of image layout.
- Separate presets, themes, and content.
- Presets own canvas dimensions, safe areas, and title geometry.
- Themes own procedural backgrounds, typography, colors, and logo treatment.
- Procedural gradients are the default background model because they scale to
  arbitrary canvas dimensions without cropping or raster degradation.
- Title fitting uses measured glyph bounds and evaluates balanced line breaks.
- Titles that cannot fit above a readable minimum size fail clearly by default.
- Infer PNG or WebP output from the output filename, with an explicit format
  override available if useful.
- Runtime behavior must not depend on POSIX shell commands, current-directory
  resource paths, or system-installed ImageMagick.
- Built-in assets must have redistribution-compatible licenses recorded in the
  repository.
- Use `ogimg` as the distribution, import, and CLI name unless a package-index
  conflict is found before publishing.
- Support Python 3.10 and newer for the initial implementation.
- Use Hatchling as the build backend and standard `pyproject.toml` metadata.
- Pillow is the only runtime dependency in the first vertical slice.
- Bundle Noto Sans Bold and its SIL Open Font License 1.1 text; load it through
  `importlib.resources` so rendering does not depend on system fonts.
- PNG determinism is tested by comparing bytes produced twice in one supported
  environment. Exact cross-version fixture hashes are deferred until the
  supported Pillow-version policy is narrower.
- Release the project under the MIT License with Ruhani Rabin
  (`https://www.ruhanirabin.com`) as the public author identity.

## Initial implementation boundary

Version one should contain:

- an installable `ogimg` command;
- `og`, `wide`, and `square` geometry presets;
- a small curated set of procedural gradient themes;
- optional PNG logo compositing with fixed placement;
- centered title layout with measured wrapping, balancing, and overflow errors;
- PNG and WebP output;
- configuration validation and actionable CLI errors;
- unit tests plus one or more deterministic render fixtures.

Base-image backgrounds, automatic subject detection, intelligent cropping,
AI-generated layouts, and platform-specific viewer launching are out of scope
for version one.

## Cross-platform constraints

- Use `pathlib` and package-resource APIs for paths.
- Avoid assumptions about executable bits, path separators, fonts installed on
  the host, and shell availability.
- Ship or deliberately acquire a redistribution-compatible font so output does
  not depend on platform font inventories.
- Test path handling and Unicode input separately from advanced script shaping.
- Use CI across Linux, macOS, and Windows before claiming verified support.

## Open decisions

- JSON-only configuration versus a later optional YAML dependency.
- Scope of complex-script shaping and bidirectional-text support in version one.
- Whether a future deterministic fixture policy pins exact pixels per supported
  Pillow version.

## Worklog convention

Use `docs/worklog/YYYY-MM-DD.md` for factual session notes. Record completed
work, verification, limitations, and links to relevant files. Keep planning and
durable decisions here rather than repeating them in every worklog.

## Related

- [Repository instructions](../AGENTS.md)
- [Initial worklog](worklog/2026-08-13.md)
