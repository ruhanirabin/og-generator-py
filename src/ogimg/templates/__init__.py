from ogimg.models import Preset, Theme

PRESETS = {
    "og": Preset(
        name="og",
        width=1200,
        height=630,
        text_box=(120, 105, 1080, 525),
        max_font_size=88,
        min_font_size=40,
        max_lines=4,
    )
}

THEMES = {
    "midnight-violet": Theme(
        name="midnight-violet",
        gradient_kind="linear",
        gradient_start=(10, 15, 35),
        gradient_end=(91, 33, 182),
        gradient_direction=(0, 1),
        gradient_center=None,
        text_color=(248, 247, 255),
        line_spacing=18,
    ),
    "graphite-indigo": Theme(
        name="graphite-indigo",
        gradient_kind="linear",
        gradient_start=(47, 39, 78),
        gradient_end=(12, 14, 28),
        gradient_direction=(1, 1),
        gradient_center=None,
        text_color=(248, 247, 250),
        line_spacing=18,
    ),
    "deep-ocean": Theme(
        name="deep-ocean",
        gradient_kind="linear",
        gradient_start=(4, 20, 34),
        gradient_end=(8, 52, 72),
        gradient_direction=(1, 0),
        gradient_center=None,
        text_color=(244, 248, 250),
        line_spacing=18,
    ),
    "ocean-orbit": Theme(
        name="ocean-orbit",
        gradient_kind="radial",
        gradient_start=(14, 67, 88),
        gradient_end=(3, 16, 30),
        gradient_direction=(0, 0),
        gradient_center=(900, 180),
        text_color=(244, 248, 250),
        line_spacing=18,
    ),
    "violet-bloom": Theme(
        name="violet-bloom",
        gradient_kind="radial",
        gradient_start=(95, 44, 170),
        gradient_end=(9, 13, 30),
        gradient_direction=(0, 0),
        gradient_center=(50, 500),
        text_color=(249, 247, 255),
        line_spacing=18,
    ),
}
