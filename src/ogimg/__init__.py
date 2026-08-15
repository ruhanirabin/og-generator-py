"""Deterministic social image generation.

Project version: resolved from the root ``VERSION`` file through package metadata.
"""

from importlib.metadata import PackageNotFoundError, version

from ogimg.render import RenderError, render_image

__all__ = ["RenderError", "render_image"]

try:
    __version__ = version("ogimg")
except PackageNotFoundError:
    __version__ = "unknown"
