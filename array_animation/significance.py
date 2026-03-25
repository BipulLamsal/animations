from manim import *
from config.brand import Config
import utils

class Significance(Scene):
    def construct(self):
        sensor_data = Config.SENSOR_DATA

        code_header = Tex(r"\textbf{Code}", font_size=24,
                          color=Config.PRIMARY_HIGHLIGHT).move_to(ORIGIN + UP * 3.2)
        horiz_div   = DashedLine(LEFT * 6.5, RIGHT * 6.5,
                                 color=GRAY_E, stroke_width=1).move_to(ORIGIN)
        mem_header  = Tex(r"\textbf{Memory}", font_size=24,
                          color=Config.PRIMARY_HIGHLIGHT).move_to(ORIGIN + DOWN * 0.6)

        self.play(FadeIn(code_header), FadeIn(horiz_div))
        utils.animate_array_declaration(self, sensor_data)

        self.play(FadeIn(mem_header))
        cells = utils.animate_array_memory(self, sensor_data, position=mem_header.get_bottom() + DOWN * 0.6)    

        self.wait(0.8)

        benefits = [
            r"Arrays always start at index \textbf{0} and not 1! Programmer love 0.",
            r"Access any element in \textbf{O(1)} time using its index eg: temp\[1\]",
            r"The size of the array is fixed prior so that memory can be allocated in a contiguous block eg: int temp\[100\]",
            r"Each element in an array is of same time so a very predictbale memory layout is possible",
            r"Iteration is easy in case of arrays",
        ]

        for i, note in enumerate(benefits):
            cell = cells[i][0]
            self.play(cell.animate.set_stroke(color=Config.PRIMARY_HIGHLIGHT, width=3), run_time=0.3)
            utils.show_note(self, note)
            self.play(cell.animate.set_stroke(color=Config.PRIMARY_HIGHLIGHT, width=1.5), run_time=0.3)

        self.wait(0.5)
        
        # cleanup
        utils.cleanup(self)