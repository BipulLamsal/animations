from manim import *
import utils

class Introduction(Scene):
    def construct(self):
        utils.centered_text_animation(
            self,
            "Think about your smartphone. You have hundreds of contacts saved. You can instantly find a name by typing just a few letters. How does that happen?"
        )
        
        utils.centered_text_animation(
            self,
            "Behind the scenes. Searching algorithms are working."
        )
