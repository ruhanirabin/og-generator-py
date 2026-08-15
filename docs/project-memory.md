# Project memory

## Goal

Create a small open-source CLI that produces polished Open Graph and article
hero images from text, procedural visual themes, and optional brand assets.

## Current baseline

- The first end-to-end vertical slice was implemented on 2026-08-13.
- It provides an installable `ogimg` command, one `og` preset, five procedural
  themes, measured balanced title fitting, clear overflow errors, and
  deterministic PNG or quality-85 WebP output.
- The primary development environment is Linux. The implementation is designed
  for Linux, macOS, and Windows, but only Linux has been verified so far.
- Optional PNG or WebP logo compositing crops transparent margins and uses
  visible aspect ratio for automatic placement: wordmarks at least 2:1 use
  `top-center`; compact logos use `top-left`. Explicit top-left, top-center, and
  top-right overrides are supported. Corner logos do not displace the title;
  centered wordmarks reserve vertical space. Configuration, additional presets
  and themes, and release automation remain future phases.
- The source repository is
  `https://github.com/ruhanirabin/og-generator-py` on the `main` branch, and
  project documentation is written for a public audience.
- The 1200×630 `og` preset meets Substack's documented minimum dimensions for
  social and post preview images as of 2026-08-13.
- When `-o` is omitted, derive a current-directory filename as
  `og-<sanitized-title>.png`; normalize Latin Unicode to ASCII, collapse other
  characters to hyphens, cap the slug at 80 characters, and use `og-image.png`
  when no ASCII slug remains.

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
  override. PNG is the default; WebP uses fixed lossy settings of quality 85
  and method 6 for social-preview delivery.
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
- Present the project as public-facing and document source installation from
  GitHub without access-status caveats.
- Determine automatic logo placement from visible alpha bounds rather than the
  source canvas: aspect ratios of 2:1 or wider are centered wordmarks; compact
  marks use the top left. Allow explicit top-left, top-center, and top-right
  overrides.
- Keep the initial theme set curated and procedural: vertical
  `midnight-violet`, diagonal `graphite-indigo`, and horizontal `deep-ocean`.
  Gradient direction and endpoint colors belong to the theme, not the preset.
- Support deterministic off-center radial themes using normalized center
  coordinates. The initial radial themes are upper-right `ocean-orbit` and
  left-origin `violet-bloom`.
- Keep batch automation external to the core renderer. The CLI remains safely
  repeatable, and a cross-platform Python helper may invoke it once per title.
- Keep the canonical project version in the root `VERSION` file. Hatchling
  reads it for distribution metadata, and runtime version reporting reads the
  installed package metadata rather than duplicating a literal version.
- Maintain `CHANGELOG.md` in Keep a Changelog format, with versions following
  Semantic Versioning and development versions expressed in PEP 440 form where
  packaging requires it.

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
