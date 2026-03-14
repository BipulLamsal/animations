from manim import *
from config.brand import Config
import utils

class Merged(Scene):
    def construct(self):
        from introduction import Introduction
        Introduction.construct(self)

        # Significance
        from significance import Significance
        Significance.construct(self)


        from indexing import Indexing
        Indexing.construct(self)