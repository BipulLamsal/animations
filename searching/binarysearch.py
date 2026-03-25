from manim import *
from config.brand import Config
import utils


class Binary(Scene):
    def construct(self):
        utils.centered_text_animation(
            self,
            "But imagine searchighng through millions of data, is it efficient to traverse all the elements sequentially?",
            wrap_width=40,
        )
        utils.centered_text_animation(
            self,
            "That's where binary search comes in."
        )

        arr = [1, 5, 6,7,9, 13, 15, 17, 20]
        TARGET = 13

        cells = utils.boxed_array(self, arr)
        self.play(
            LaggedStart(
                *[FadeIn(cell) for cell in cells],
                lag_ratio=0.20
            )
        )

        utils.show_note(self, "We have a sorted array and we want to search for 13 using binary search")
        utils.show_note(self, "Get to the middle and compare that selected key; go left if smaller, right if larger")

        pointer = Arrow(
            start=LEFT * 0.6, end=RIGHT * 0.01,
            color=Config.PRIMARY_HIGHLIGHT, buff=0,
            max_tip_length_to_length_ratio=0.2,
            stroke_width=4,
        )

        low, high = 0, len(arr) - 1
        first = True

        while low <= high:
            mid = (low + high) // 2

            if first:
                pointer.next_to(cells[mid], LEFT, buff=0.15)
                self.play(FadeIn(pointer))
                first = False
            else:
                self.play(pointer.animate.next_to(cells[mid], LEFT, buff=0.15), run_time=0.4)

            rect = cells[mid][0]
            self.play(rect.animate.set_fill(color=Config.SECONDARY_ACCENT, opacity=1), run_time=0.3)
            self.wait(0.3)

            if arr[mid] == TARGET:
                self.play(rect.animate.set_fill(color=Config.PRIMARY_HIGHLIGHT, opacity=0.2), run_time=0.3)
                utils.show_note(self, f"Found '{TARGET}' at index {mid}!")
                break
            
            elif arr[mid] > TARGET:
                # ignoring the right half
                for i in range(mid, high + 1):
                    self.play(cells[i][0].animate.set_fill(color=Config.SECONDARY_ACCENT, opacity=1),
                              cells[i][1].animate.set_opacity(0.2), run_time=0.12)
                utils.show_note(self, "the index value is heigher than the key so we search left half")
                high = mid - 1
            else:
                # ignoring the left side
                for i in range(low, mid + 1):
                    self.play(cells[i][0].animate.set_fill(color=Config.SECONDARY_ACCENT, opacity=1),
                              cells[i][1].animate.set_opacity(0.2), run_time=0.12)
                utils.show_note(self, "the index value is smaller than the key so we search right half")
                low = mid + 1

        self.wait(1)
        utils.cleanup(self)
        
        overlay = Circle(radius=8.0,
            fill_color=Config.SECONDARY_ACCENT,
            fill_opacity=0.0,
            stroke_width=0
        ).move_to(ORIGIN)

        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=0.85), run_time=0.4)

        utils.centered_text_animation(
                    self,
                "It was relatively faster to search the key this way because we keep ignoring half of items in each comparison.",
                wrap_width=45,
        )

        definition = r"Binary search is an efficient searching algorithm that finds the position of a target value within a sorted array. It works by repeatedly dividing the search interval in half, which drastically reduces the number of comparisons needed compared to a linear search."
        utils.bullet_definition(self, definition, overlay=overlay)
        
        utils.cleanup(self)
        
        
        cells = utils.boxed_array(self, arr)
        self.play(
            LaggedStart(
                *[FadeIn(cell) for cell in cells],
                lag_ratio=0.20
            )
        )
        
        utils.show_note(self, "Searching elements in binary take O(log n) meaning we have two choices and ignore one of them. log here is base 2.")
        utils.show_note(self, "Searching elements in linear take O(n) meaning we have to check each element one by one.")
        
        
        