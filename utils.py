
from manim import *
from config.brand import Config
import textwrap


def centered_text_animation(scene: Scene, content: str,
                             font_size: int = 40,
                             wrap_width: int = 40,
                             wait_time: float = 2.0,
                             run_time: float = 3.0):
    lines = textwrap.wrap(content, width=wrap_width)
 
    group = VGroup(*[
        Tex(line, font_size=font_size, color=Config.PRIMARY_HIGHLIGHT)
        for line in lines
    ])
 
    group.arrange(DOWN, center=True, buff=0.20)
    group.move_to(ORIGIN)
 
    scene.play(Write(group, run_time=run_time))
    scene.wait(wait_time)
    scene.play(FadeOut(group))
    return group

def create_header(label_text, font_size: int = 32,):
    header_text = MathTex(label_text, color=Config.PRIMARY_HIGHLIGHT, font_size=font_size)
    box = SurroundingRectangle(header_text, buff=0.4, color=WHITE, stroke_width=2)
    
    dash = DashedLine(
        start=box.get_left(), 
        end=box.get_right(), 
        stroke_width=2
    ).next_to(box, DOWN, buff=0)
    
    return VGroup(box, header_text, dash)


def create_memory_stack(num_slots=10, cell_w=3, cell_h=0.5, corner=0.1):
    stack = VGroup()
    for i in range(num_slots):
        cell = RoundedRectangle(
            corner_radius=corner,
            width=cell_w, height=cell_h,
            color=Config.PRIMARY_HIGHLIGHT,
            fill_color=Config.SECONDARY_ACCENT,
            fill_opacity=0.0,
            stroke_width=1.5
        )
        stack.add(cell)
    stack.arrange(DOWN, buff=0)
    return stack

def stack_fill(scene: Scene, stack: VGroup, index: int, value: str, font_size: int = 22, runtime: float = 0.5):
    cell = stack[index]
    cell.set_fill(opacity=0.0)  # transition from transparent
    text = Tex(value, font_size=font_size, color=Config.PRIMARY_HIGHLIGHT)
    text.move_to(cell.get_center())
    scene.play(
        cell.animate.set_fill(opacity=0.25),
        FadeIn(text, shift=DOWN * 0.2),
        run_time=runtime
    )
    return text

def show_note(scene: Scene, message: str, wait: float = 1.8, font_size: int = 22, runtime: float = 1):
    txt = Tex(message, font_size=font_size, color=Config.TEXT_COLOR)
    bg  = RoundedRectangle(
        corner_radius=0.3,
        width=txt.width + 1.0,
        height=txt.height + 0.6,
        fill_color=Config.SECONDARY_ACCENT,
        fill_opacity=0.95,
        color=Config.PRIMARY_HIGHLIGHT,
        stroke_width=2
    )
    txt.move_to(bg)
    note = VGroup(bg, txt).to_edge(DOWN, buff=0.3)
    note.shift(DOWN * 2)  # start off screen

    scene.play(note.animate.shift(UP * 2), run_time=runtime)
    scene.wait(wait)
    scene.play(note.animate.shift(DOWN * 2), run_time=runtime)
    
    
    
def bullet_definition(scene: Scene, definition: str, font_size: int = 32, overlay: Circle = None):
    
    big_circle = overlay if overlay is not None else Circle(
        radius=6.0,
        fill_color=Config.SECONDARY_ACCENT,
        fill_opacity=0.85,
        stroke_width=0
    ).move_to(ORIGIN)

    small_circle = Circle(
        radius=0.18,
        fill_color=Config.PRIMARY_HIGHLIGHT,
        fill_opacity=1.0,
        stroke_width=0
    ).move_to(ORIGIN)

    # collapse overlay into small bullet
    scene.play(Transform(big_circle, small_circle), run_time=0.6)


    # pulse
    scene.play(big_circle.animate.scale(2.5), run_time=0.15)
    scene.play(big_circle.animate.scale(0.4), run_time=0.15)

    # definition box
    txt = Tex(definition, font_size=font_size, color=Config.TEXT_COLOR)
    box = RoundedRectangle(
        corner_radius=0.3,
        width=txt.width + 1.0,
        height=txt.height + 0.6,
        fill_color=Config.SECONDARY_ACCENT,
        fill_opacity=0.9,
        color=Config.PRIMARY_HIGHLIGHT,
        stroke_width=1.8
    )
    txt.move_to(box)
    def_grp = VGroup(box, txt)


    bullet_pos = ORIGIN + LEFT * (def_grp.width / 2 + 0.30)
    def_grp.move_to(ORIGIN + RIGHT * 0.25)

    scene.play(
        big_circle.animate.move_to(bullet_pos),
        FadeIn(def_grp, shift=RIGHT * 0.2),
        run_time=0.6
    )
    scene.wait(2.0)
    return VGroup(big_circle, def_grp)


def boxed_array(scene: Scene, data: list):
    preview = data[:]

    CELL_W, CELL_H = 2.5, 0.7  
    PADDING = 0.20

    boxes = VGroup()

    for item in preview:
        # outer box
        rect = Rectangle(
            width=CELL_W,
            height=CELL_H,
            stroke_color=Config.PRIMARY_HIGHLIGHT,
            fill_color=Config.SECONDARY_ACCENT,
            fill_opacity=0.8,
        )

        txt = Tex(str(item), font_size=24, color=Config.PRIMARY_HIGHLIGHT)

        # left alignment of text inside the box
        txt.align_to(rect.get_left() + RIGHT * PADDING, LEFT)
        txt.move_to([txt.get_x(), rect.get_center()[1], 0])

        # group
        element = VGroup(rect, txt)
        boxes.add(element)

    boxes.arrange(DOWN, buff=0)
    boxes.move_to(ORIGIN)

    return boxes


def animate_array_declaration(scene: Scene, data: list):
    preview = data[:5]
    vals_str = ', '.join(str(v) for v in preview) + ', ...'

    part1 = Tex(r"int\ temp[]\ =\ (", font_size=28, color=Config.PRIMARY_HIGHLIGHT)
    part2 = Tex(vals_str, font_size=28, color=Config.TEXT_COLOR)
    part3 = Tex(r");", font_size=28, color=Config.TEXT_COLOR)

    part2.next_to(part1, RIGHT, buff=0.04)
    part3.next_to(part2, RIGHT, buff=0.04)

    line = VGroup(part1, part2, part3)
    line.move_to(ORIGIN + UP * 1.5)
    scene.play(Write(line), run_time=1.2)
    return line


def animate_array_memory(scene: Scene, data: list, position=ORIGIN):
    CELL_W, CELL_H = 1.3, 0.55
    BASE_ADDR, STEP = 100, 4
    preview = data[:5]

    cells = VGroup()
    for i, val in enumerate(preview):
        cell  = RoundedRectangle(corner_radius=0.1, width=CELL_W, height=CELL_H,
                                 color=Config.PRIMARY_HIGHLIGHT,
                                 fill_color=Config.SECONDARY_ACCENT,
                                 fill_opacity=0.25, stroke_width=1.5)
        value = Tex(str(val), font_size=22, color=Config.TEXT_COLOR)
        addr  = Tex(str(BASE_ADDR + i * STEP), font_size=13, color=Config.TEXT_COLOR)
        idx   = Tex(rf"[{i}]", font_size=13, color=Config.PRIMARY_HIGHLIGHT)
        value.move_to(cell.get_center())
        addr.next_to(cell, UP,   buff=0.1)
        idx.next_to(cell,  DOWN, buff=0.1)
        cells.add(VGroup(cell, value, addr, idx))

    cells.arrange(RIGHT, buff=0)
    cells.move_to(position)  # position BEFORE animating

    scene.play(
        LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cells], lag_ratio=0.12),
        run_time=0.8
    )
    return cells


def cleanup(scene: Scene):
          scene.play(
            *[FadeOut(mob) for mob in scene.mobjects],
            run_time=0.5
        )