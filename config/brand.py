from manim import config as mc
from manim import WHITE, BLACK, register_font


class Config:
    mc.background_color = WHITE
    register_font("Arial")

    PRIMARY_HIGHLIGHT = "#db2777"
    SECONDARY_ACCENT = "#fce7f3"

    TEXT_COLOR = BLACK
    FONT = "Arial"

    MIN_GAP = 0.5

    HEADER_BG = "#111111"
    HEADER_TEXT = WHITE

    LEFT_MARGIN = 0.7
    TOP_MARGIN = 0.5
    
    SENSOR_DATA = [27, 29, 30, 28, 31, 26, 27, 29, 30, 28, 31, 26, 27, 29, 30, 28, 31, 26]  
