from manim import *
from config.brand import Config
import utils


class Linear(Scene):
    def construct(self):
        arr = utils.boxed_array(self, Config.CONTACTS)
        self.play(
            LaggedStart(
                *[FadeIn(cell) for cell in arr],
                lag_ratio=0.20
            )
        )

        utils.show_note(self, "Now lets say you searched for 'Nir' on your contacts")

        pointer = Arrow(
            start=LEFT * 0.6, end=RIGHT * 0.01,
            color=Config.PRIMARY_HIGHLIGHT, buff=0,
            max_tip_length_to_length_ratio=0.2,
            stroke_width=4,
        )
        pointer.next_to(arr[0], LEFT, buff=0.15)
        self.play(FadeIn(pointer))

        preview = Config.CONTACTS[:5]

        for i, cell in enumerate(arr):
            rect = cell[0]

            self.play(pointer.animate.next_to(cell, LEFT, buff=0.15), run_time=0.4)

            self.play(rect.animate.set_fill(color= Config.SECONDARY_ACCENT,opacity=1), run_time=0.3)
            self.wait(0.3)

            if "nir" in str(preview[i]).lower():
                self.play(rect.animate.set_fill(color=Config.PRIMARY_HIGHLIGHT, opacity=0.2), run_time=0.3)
                utils.show_note(self, f"Found : '{preview[i]}' at index {i}!")
                break
           
        self.wait(1)
        utils.show_note(self, "See how our phone checked the contact serailly from first to last until we found 'Nir' ?")
        utils.show_note(self, "Ofcourse this is not how phones actually search contacts but this is the most basic way to search something in a list of items!")
        utils.cleanup(self)
        
        overlay = Circle(radius=8.0,
            fill_color=Config.SECONDARY_ACCENT,
            fill_opacity=0.0,
            stroke_width=0
        ).move_to(ORIGIN)

        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=0.85), run_time=0.4)

        banner = Tex(r"This is the basic algorithm of searching items known as Linear Search",
                    font_size=42, color=Config.PRIMARY_HIGHLIGHT)
        self.play(Write(banner), run_time=0.6)
        self.wait(1.5)

        # clear everything except overlay
        self.play(
            FadeOut(banner),
            *[FadeOut(mob) for mob in self.mobjects if mob is not overlay],
            run_time=0.5
        )

        definition = r"Linear or Sequential search is a straightforward algorithm for finding a specific value within a list by systematically examining each element one by one, starting from the beginning of the list."
        utils.bullet_definition(self, definition, overlay=overlay)
        
        utils.cleanup(self)
        
        