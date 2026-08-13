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
        gradient_start=(10, 15, 35),
        gradient_end=(91, 33, 182),
        text_color=(248, 247, 255),
        line_spacing=18,
    )
}
