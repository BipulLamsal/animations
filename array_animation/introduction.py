from manim import *
import random
from config.brand import Config
import utils


class Introduction(Scene):
    def construct(self):
        utils.centered_text_animation(
            self, "We have a sensor collecting temperature readings every day for 365 days")

        utils.centered_text_animation(
            self, "Our program saves each sensor data in seperate variables")

        sensor_data = Config.SENSOR_DATA
        left_header = utils.create_header("Code").shift(LEFT * 3.5 + UP * 3)
        right_header = utils.create_header("Memory").shift(RIGHT * 3.5 + UP * 3)
        vertical_div = DashedLine(
            start=UP * 4, 
            end=DOWN * 4, 
            color=GRAY_E, 
            stroke_width=1
        )
        
        self.play(FadeIn(left_header), FadeIn(right_header), FadeIn(vertical_div))
        
        start_x_point = left_header.get_left()

        last_line = left_header
        start_x   = left_header.get_left()
        
        stack = utils.create_memory_stack()
        stack.move_to([right_header.get_center()[0], 0, 0])

        self.play(Create(stack))

        for i, val in enumerate(sensor_data[:5]):
            var  = Tex(rf"int\ day{i+1}", font_size=28, color=GREY_D)
            eq   = Tex(r"\ =\ ",          font_size=28, color=Config.SECONDARY_ACCENT)
            rest = Tex(rf"{val};",         font_size=28, color=Config.PRIMARY_HIGHLIGHT)
            
            eq.next_to(var,  RIGHT, buff=0.04)
            rest.next_to(eq, RIGHT, buff=0.04)

            line = VGroup(var,eq, rest) # grouped them
            if i == 0:
                # first line centers under the header rest is just left alignemnt
                line.next_to(last_line, DOWN, buff=0.4)
                line.move_to([left_header.get_center()[0], line.get_center()[1], 0])
                start_x = line.get_left()  # lock left edge from first line
            else:
                # rest align to first line's left edge
                line.next_to(last_line, DOWN, buff=0.4).align_to(start_x, LEFT)

            self.play(Write(line), run_time=2.0)
            last_line = line
            if i < 3:
                utils.stack_fill(self, stack, i, str(val))
            elif i == 3:
                # fill 3 gap cells first
                for j in range(3):
                    utils.stack_fill(self, stack, 3 + j, "...")
                # then resume value after the gap
                utils.stack_fill(self, stack, 6, str(val))
            else:
                utils.stack_fill(self, stack, i + 3, str(val))
            

        dots = Tex(r"\vdots", font_size=32, color=GRAY_D)
        dots.next_to(last_line, DOWN, buff=0.3).align_to(start_x, LEFT).shift(RIGHT * 0.2)
        self.play(Write(dots))
        
        utils.show_note(self, r"Notice how difficult it is to maintain such a large number of variables")
        utils.show_note(self, r"Variables may not be stored contiguously  depending upon the OS")
        utils.show_note(self, r"The ... as seen int the memory is reprentation of fragmentation")
        
        overlay = Circle(radius=8.0,
            fill_color=Config.SECONDARY_ACCENT,
            fill_opacity=0.0,
            stroke_width=0
        ).move_to(ORIGIN)

        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=0.85), run_time=0.4)

        banner = Tex(r"That's where \textbf{Arrays} come in!",
                    font_size=42, color=Config.PRIMARY_HIGHLIGHT)
        self.play(Write(banner), run_time=0.6)
        self.wait(1.5)

        # clear everything except overlay
        self.play(
            FadeOut(banner),
            *[FadeOut(mob) for mob in self.mobjects if mob is not overlay],
            run_time=0.5
        )

        definition = r"An \textbf{Array} is a data structure that stores a collection of elements, typically of the same type, in contiguous memory locations. It allows for efficient access and manipulation of data using an index."
        utils.bullet_definition(self, definition, overlay=overlay)
        self.wait()