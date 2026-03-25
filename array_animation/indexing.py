from manim import *
from config.brand import Config
import utils

class Indexing(Scene):
    def construct(self):
        sensor_data = Config.SENSOR_DATA[:5]
        cells = utils.animate_array_memory(self, sensor_data)
        self.wait(0.4)
        
        utils.show_note(self, r"An array name \textbf{temp} is just a pointer to the first element meaning the memory location of first element of array is same as the memory location of the array itself")
        utils.show_note(self, r"A pointer holds a \textbf{memory address} in our case temp (which is a reference to first element) stores address 100 and *temp and temp[0] are same and give us the value at address 100")

        arrow = Arrow(
            cells[0].get_top() + UP * 0.6,
            cells[0].get_top() + UP * 0.1,
            color=Config.PRIMARY_HIGHLIGHT,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.25
        )
        ptr_label = Tex(r"temp[0]", font_size=26, color=Config.PRIMARY_HIGHLIGHT)
        ptr_label.next_to(arrow.get_start(), UP, buff=0.15)

        self.play(Create(arrow), FadeIn(ptr_label), run_time=0.5)
        cells[0][0].set_stroke(color=Config.SECONDARY_ACCENT, width=3)
        utils.show_note(self, rf"$100 + 0 \times 4 = 100$ $\rightarrow$ {sensor_data[0]}")
        self.wait(0.2)

        for i in range(1, len(sensor_data)):
            val       = sensor_data[i]
            shift_x   = cells[i].get_center()[0] - arrow.get_center()[0]
            new_label = Tex(rf"temp[{i}]", font_size=26, color=Config.PRIMARY_HIGHLIGHT)
            new_label.next_to(cells[i].get_top() + UP * 0.6, UP, buff=0.15)

            self.play(
                arrow.animate.shift(RIGHT * shift_x),
                Transform(ptr_label, new_label),
                cells[i][0].animate.set_stroke(color=Config.SECONDARY_ACCENT, width=3),
                cells[i-1][0].animate.set_stroke(color=Config.PRIMARY_HIGHLIGHT, width=1.5),
                run_time=0.55
            )
            utils.show_note(self, rf"$100 + {i} \times 4 = {100 + i * 4}$ $\rightarrow$ {val}")
            self.wait(0.2)

        self.play(
            FadeOut(arrow), FadeOut(ptr_label),
            cells[4][0].animate.set_stroke(color=Config.PRIMARY_HIGHLIGHT, width=1.5),
            run_time=0.4
        )

        formula = MathTex(
            r"\text{temp}[i] = 100 + i \times ", r"4",
            font_size=30, color=Config.TEXT_COLOR
        ).move_to(UP * 2.5)
        self.play(Write(formula), run_time=0.8)

        circle = Circle(radius=0.3, color=Config.PRIMARY_HIGHLIGHT,
                        stroke_width=2).move_to(formula[1].get_center())
        self.play(Create(circle), run_time=0.6)

        utils.show_note(self, r"All elements are \textbf{same type} so pointer knows exactly how far to jump")
        utils.show_note(self, r"In our case the elements are int and its size is \textbf{4 bytes} array jumps 4bytes at a time to access next element")

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)