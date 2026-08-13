# AGENTS.md

## Purpose

Build `ogimg`, a deterministic Python CLI that generates template-based social
images from text, procedural backgrounds, and an optional logo. The project is
intended to be installable and usable on Linux, macOS, and Windows.

## Read first

Before material changes, read:

1. `docs/project-memory.md`
2. the latest file in `docs/worklog/`
3. the source and tests relevant to the task

## Repository map

- `src/ogimg/` — application and rendering code.
- `tests/` — automated tests; mirror source responsibilities where practical.
- `src/ogimg/templates/` — built-in canvas presets and visual themes shipped
  with the package.
- `docs/project-memory.md` — durable decisions, constraints, and open questions.
- `docs/worklog/` — concise, dated records of material work sessions.
- `examples/` — public example inputs and generated-output documentation.

## Working rules

- Keep rendering deterministic: identical inputs and versions produce identical
  pixels.
- Keep geometry (`preset`), appearance (`theme`), and user content separate.
- Procedural backgrounds are the default. Do not add raster base images to the
  core template model without a recorded decision.
- Measure rendered glyphs for wrapping and fitting; never infer fit from
  character count.
- Reject unreadable overflow by default. Do not silently truncate titles.
- Keep the core cross-platform and avoid shell-only runtime behavior.
- Resolve bundled resources through Python package APIs, not the current
  working directory.
- Do not commit generated images, virtual environments, caches, build output,
  local configuration, or proprietary brand assets.
- Add dependencies only when they remove meaningful complexity. Keep optional
  features optional.
- Preserve unrelated user changes.

## Verification

Run the narrowest relevant checks during development. Before handoff, run when
available:

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m build
git diff --check
```

Record unavailable checks and platform-specific limits in the worklog.

## Documentation

- Add `docs/worklog/YYYY-MM-DD.md` after a material work session.
- Update `docs/project-memory.md` only when a durable fact, decision, risk, or
  open question changes.
- Keep worklogs factual: changed, verified, not verified, and related paths.

## Publishing boundary

Do not publish packages, create releases, push commits, or change external
services without explicit approval. Never claim cross-platform support from a
single-platform test; distinguish designed support from verified support.

## SilverBullet project record

After meaningful architecture, implementation, release, or project-documentation
milestones, read `/home/rabin/remote-sync/silverbullet/AGENTS.md`, then update:

- `/home/rabin/remote-sync/silverbullet/Projects/OG Image Generator CLI.md`
- `/home/rabin/remote-sync/silverbullet/Journal/Daily/YYYY-MM-DD.md`

Preserve frontmatter and `[[Wiki Links]]`. Record only durable outcomes and
verification evidence; do not copy raw logs or private brand assets.

## Git hygiene

Use Conventional Commits 1.0.0. Keep commits coherent and inspect the complete
staged diff before committing.
