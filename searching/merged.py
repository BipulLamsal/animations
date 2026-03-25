from manim import *
from config.brand import Config
import utils
from introduction import Introduction
from linearsearching import Linear
from binarysearch import Binary


class Merged(Scene):
    def construct(self):
        Introduction.construct(self)
        Linear.construct(self)
        Binary.construct(self)