# array by defination and we just debunk afterwards
# we talk about variables and poitners how everythign works under the hood
# we needd how data are stored in the memory
# creating differnet vairbales
# showing different pointer for each variable
# they are stored in stack
# now what is stack?
# what is heap?
# alright we now know that variables are distrubuted in random location?
# is it good for optimization picking up different location each time brings overhead maybe idk?
# now that since the variables we created are of same type can we can defieinlrt merge them in a same memroy location
# this is where array comes in

from manim import *

config.background_color = WHITE

PRIMARY_HIGHLIGHT = "#db2777"
SECONDARY_ACCENT = "#fce7f3"
TEXT_COLOR = BLACK
MIN_GAP = 0.5

HEADER_BG = "#111111"
HEADER_TEXT = WHITE


def title_text(txt, size=38, color=TEXT_COLOR):
    return Text(txt, font_size=size, color=color, weight=BOLD)


def body_text(txt, size=26, color=TEXT_COLOR):
    return Text(txt, font_size=size, color=color)


def small_text(txt, size=20, color=TEXT_COLOR):
    return Text(txt, font_size=size, color=color)


def code_text(txt, size=25, color=TEXT_COLOR):
    return Text(txt, font="Consolas", font_size=size, color=color)


def make_header(title):
    bg = Rectangle(
        width=14.2,
        height=0.8,
        fill_color=HEADER_BG,
        fill_opacity=1,
        stroke_width=0
    ).to_edge(UP)
    txt = Text(title, font_size=30, color=HEADER_TEXT, weight=BOLD)
    txt.move_to(bg.get_center())
    return VGroup(bg, txt)


def variable_card(name, value, width=2.45, height=0.95):
    box = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=PRIMARY_HIGHLIGHT,
        stroke_width=2,
        fill_color=SECONDARY_ACCENT,
        fill_opacity=0.95
    )
    t1 = code_text(name, size=23, color=TEXT_COLOR)
    t2 = code_text(f"= {value}", size=23, color=PRIMARY_HIGHLIGHT)
    grp = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
    grp.move_to(box.get_center())
    return VGroup(box, grp)


def memory_block(value="", address="", width=1.45, height=0.95):
    rect = Rectangle(
        width=width,
        height=height,
        stroke_color=BLACK,
        stroke_width=1.5,
        fill_color="#f8fafc",
        fill_opacity=1
    )
    val = code_text(str(value), size=22, color=TEXT_COLOR)
    val.move_to(rect.get_center())
    addr = Text(str(address), font_size=17, color=GRAY)
    addr.next_to(rect, DOWN, buff=0.08)
    return VGroup(rect, val, addr)


def array_block(value, index=None, width=1.3, height=0.95):
    rect = Rectangle(
        width=width,
        height=height,
        stroke_color=PRIMARY_HIGHLIGHT,
        stroke_width=2,
        fill_color=SECONDARY_ACCENT,
        fill_opacity=0.95
    )
    val = code_text(str(value), size=22, color=TEXT_COLOR)
    val.move_to(rect.get_center())
    if index is not None:
        idx = Text(str(index), font_size=18, color=GRAY)
        idx.next_to(rect, DOWN, buff=0.08)
        return VGroup(rect, val, idx)
    return VGroup(rect, val)


def pointer_box(name="p", value="1000", width=2.4, height=0.95):
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=BLUE,
        stroke_width=2,
        fill_color="#dbeafe",
        fill_opacity=0.95
    )
    t1 = code_text(name, size=23, color=BLUE)
    t2 = code_text(f"= {value}", size=23, color=TEXT_COLOR)
    grp = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
    grp.move_to(rect.get_center())
    return VGroup(rect, grp)


def panel(lines, width=5.2, height=2.0, fill="#ffffff", stroke="#d1d5db"):
    rect = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=1.5,
        fill_color=fill,
        fill_opacity=1
    )
    txts = VGroup(*[body_text(line, size=23) for line in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.12
    )
    txts.move_to(rect.get_center())
    return VGroup(rect, txts)


class ArrayCompleteIntro(Scene):
    def construct(self):
        header = make_header("Arrays in C")
        self.play(FadeIn(header), run_time=0.7)

        marks = [78, 85, 91, 67, 88]

        # -------------------------------------------------
        # 1. Real-life situation
        # -------------------------------------------------
        t1 = title_text(
            "Suppose we want to store marks of 5 students", size=34)
        t1.next_to(header, DOWN, buff=0.55)
        self.play(Write(t1), run_time=0.9)

        students = VGroup(*[
            variable_card(f"Student {i+1}", marks[i], width=2.1, height=0.9)
            for i in range(5)
        ])
        students.arrange(RIGHT, buff=0.22)
        students.scale(0.92)
        students.move_to(ORIGIN + DOWN*0.8)

        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.1)
                  for s in students], lag_ratio=0.12), run_time=1.1)

        note = body_text("This looks fine for a few values.",
                         size=25, color=PRIMARY_HIGHLIGHT)
        note.to_edge(DOWN).shift(UP*0.4)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(students), FadeOut(note), FadeOut(t1), run_time=0.8)

        # -------------------------------------------------
        # 2. Problem with many variables
        # -------------------------------------------------
        t2 = title_text("But what if there are 100 or 1000 values?", size=34)
        t2.next_to(header, DOWN, buff=0.55)
        self.play(Write(t2), run_time=0.8)

        vars_group = VGroup(
            variable_card("mark1", 78),
            variable_card("mark2", 85),
            variable_card("mark3", 91),
            variable_card("mark4", 67),
            variable_card("mark5", 88),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).scale(0.82)
        # Move the whole group
        vars_group.to_edge(LEFT)  # move to the left edge
        vars_group.shift(RIGHT*0.7 + DOWN*0.2)  # fine-tune position

        extra_names = VGroup(
            code_text("mark6", size=23),
            code_text("mark7", size=23),
            code_text("mark8", size=23),
            code_text("...", size=24, color=PRIMARY_HIGHLIGHT),
            code_text("mark1000", size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        extra_names.next_to(vars_group, RIGHT, buff=1.2)

        issues = panel(
            ["Too many names",
             "Hard to manage",
             "Hard to search together"],
            width=4.8,
            height=2.0,
            fill="#fff7ed",
            stroke="#fdba74"
        )
        issues.to_edge(RIGHT).shift(LEFT*0.7 + DOWN*0.3)

        self.play(LaggedStart(*[FadeIn(v, shift=RIGHT*0.1)
                  for v in vars_group], lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(extra_names), FadeIn(issues), run_time=0.8)
        self.wait(1.3)

        self.play(FadeOut(extra_names), FadeOut(
            issues), FadeOut(t2), run_time=0.7)

        # -------------------------------------------------
        # 3. Separate variables in memory
        # -------------------------------------------------
        t3 = title_text(
            "Separate variables can appear separately in memory", size=31)
        t3.next_to(header, DOWN, buff=0.55)
        self.play(Write(t3), run_time=0.8)

        mem_col = VGroup(
            memory_block(78, 1008),
            memory_block(85, 2032),
            memory_block(91, 1176),
            memory_block(67, 3096),
            memory_block(88, 4120),
        ).arrange(DOWN, buff=0.28)
        mem_col.to_edge(RIGHT)
        mem_col.shift(LEFT*0.95 + DOWN*0.15)

        mem_label = body_text("Memory", size=26)
        mem_label.next_to(mem_col, UP, buff=0.2)

        self.play(FadeIn(mem_label), FadeIn(mem_col), run_time=0.9)

        arrows = VGroup(*[
            Arrow(vars_group[i].get_right(), mem_col[i].get_left(),
                  buff=0.12, stroke_color=PRIMARY_HIGHLIGHT)
            for i in range(5)
        ])
        self.play(LaggedStart(*[GrowArrow(a)
                  for a in arrows], lag_ratio=0.08), run_time=1.0)

        q1 = body_text("Can related data be kept together instead?",
                       size=26, color=PRIMARY_HIGHLIGHT)
        q1.to_edge(DOWN).shift(UP*0.4)
        self.play(Write(q1), run_time=0.7)
        self.wait(1.3)

        self.play(
            FadeOut(vars_group), FadeOut(mem_col), FadeOut(mem_label),
            FadeOut(arrows), FadeOut(q1), FadeOut(t3),
            run_time=0.8
        )

        # -------------------------------------------------
        # 4. Array introduction
        # -------------------------------------------------
        t4 = title_text("Yes. That is exactly what an array does.", size=33)
        t4.next_to(header, DOWN, buff=0.55)
        self.play(Write(t4), run_time=0.8)

        c_decl = code_text("int marks[5] = {78, 85, 91, 67, 88};", size=29)
        c_decl.move_to(ORIGIN + UP*0.35)
        self.play(Write(c_decl), run_time=1.0)

        arr_row = VGroup(*[array_block(v, i)
                         for i, v in enumerate(marks)]).arrange(RIGHT, buff=0)
        arr_row.move_to(ORIGIN + DOWN*0.8)

        arr_cap = body_text(
            "One name stores multiple values of the same type", size=24, color=PRIMARY_HIGHLIGHT)
        arr_cap.next_to(arr_row, UP, buff=0.25)

        self.play(TransformFromCopy(c_decl, arr_row), run_time=1.0)
        self.play(FadeIn(arr_cap), run_time=0.6)
        self.wait(1.2)

        self.play(FadeOut(c_decl), FadeOut(arr_cap), FadeOut(t4), run_time=0.7)

        # -------------------------------------------------
        # 5. Contiguous memory
        # -------------------------------------------------
        t5 = title_text(
            "Array elements are stored in contiguous memory", size=31)
        t5.next_to(header, DOWN, buff=0.55)
        self.play(Write(t5), run_time=0.8)

        mem_row = VGroup(
            memory_block(78, 1000),
            memory_block(85, 1004),
            memory_block(91, 1008),
            memory_block(67, 1012),
            memory_block(88, 1016),
        ).arrange(RIGHT, buff=0)
        mem_row.move_to(ORIGIN + DOWN*0.1)

        self.play(Transform(arr_row, mem_row), run_time=1.1)

        brace = Brace(mem_row, DOWN, color=PRIMARY_HIGHLIGHT)
        brace_text = body_text(
            "Contiguous memory = next to each other", size=24, color=PRIMARY_HIGHLIGHT)
        brace_text.next_to(brace, DOWN, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(brace_text), run_time=0.8)
        self.wait(1.4)

        self.play(FadeOut(brace), FadeOut(
            brace_text), FadeOut(t5), run_time=0.7)

        # -------------------------------------------------
        # 6. Base address and indexing
        # -------------------------------------------------
        t6 = title_text("The array starts from a base address", size=32)
        t6.next_to(header, DOWN, buff=0.55)
        self.play(Write(t6), run_time=0.8)

        arr_name = code_text("marks", size=29, color=PRIMARY_HIGHLIGHT)
        arr_name.next_to(mem_row, LEFT, buff=1.3)
        arr_arrow = Arrow(arr_name.get_right(),
                          mem_row[0].get_left(), buff=0.1)
        base_text = body_text("Base address = 1000", size=25)
        base_text.next_to(mem_row, UP, buff=0.35)

        self.play(Write(arr_name), GrowArrow(arr_arrow), run_time=0.9)
        self.play(FadeIn(base_text), run_time=0.6)

        formula = VGroup(
            code_text("marks[0] -> 1000", size=23),
            code_text("marks[1] -> 1004", size=23),
            code_text("marks[2] -> 1008", size=23),
            code_text("Address = base + i × size",
                      size=23, color=PRIMARY_HIGHLIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        formula.to_edge(DOWN).shift(UP*0.4)

        self.play(FadeIn(formula), run_time=0.8)

        for i in range(3):
            h = SurroundingRectangle(
                mem_row[i][0], color=PRIMARY_HIGHLIGHT, buff=0.04)
            self.play(Create(h), run_time=0.35)
            self.wait(0.15)
            self.play(FadeOut(h), run_time=0.2)

        self.wait(1.2)
        self.play(FadeOut(t6), FadeOut(base_text),
                  FadeOut(formula), run_time=0.7)

        # -------------------------------------------------
        # 7. Searching
        # -------------------------------------------------
        t7 = title_text("Searching in an array becomes systematic", size=31)
        t7.next_to(header, DOWN, buff=0.55)
        self.play(Write(t7), run_time=0.8)

        sub7 = body_text("Let's find 67", size=26, color=PRIMARY_HIGHLIGHT)
        sub7.next_to(t7, DOWN, buff=0.18)
        self.play(FadeIn(sub7), run_time=0.6)

        status = body_text("Checking elements one by one", size=24)
        status.to_edge(DOWN).shift(UP*0.4)
        self.play(FadeIn(status), run_time=0.6)

        for i, v in enumerate(marks):
            box = SurroundingRectangle(
                mem_row[i][0], color=PRIMARY_HIGHLIGHT, buff=0.05)
            txt = code_text(f"marks[{i}] = {v}", size=23)
            txt.next_to(status, UP, buff=0.14)
            self.play(Create(box), FadeIn(txt), run_time=0.45)
            self.wait(0.25)
            if v == 67:
                found = body_text("Found at index 3", size=25, color=GREEN)
                found.next_to(status, DOWN, buff=0.14)
                self.play(FadeIn(found), run_time=0.5)
                self.wait(1.0)
                self.play(FadeOut(found), FadeOut(box),
                          FadeOut(txt), run_time=0.3)
                break
            else:
                self.play(FadeOut(box), FadeOut(txt), run_time=0.25)

        loop_note = body_text(
            "That is why arrays work very well with loops.", size=24, color=PRIMARY_HIGHLIGHT)
        loop_note.next_to(sub7, DOWN, buff=0.28)
        self.play(FadeIn(loop_note), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(t7), FadeOut(sub7), FadeOut(
            status), FadeOut(loop_note), run_time=0.7)

        # -------------------------------------------------
        # 8. Array vs pointer
        # -------------------------------------------------
        t8 = title_text(
            "Important: an array is not the same as a pointer", size=31)
        t8.next_to(header, DOWN, buff=0.55)
        self.play(Write(t8), run_time=0.8)

        divider = Line(UP*2.5, DOWN*2.5, color=LIGHT_GRAY)
        divider.move_to(ORIGIN)

        left_title = body_text("Array", size=27, color=PRIMARY_HIGHLIGHT)
        right_title = body_text("Pointer", size=27, color=BLUE)

        left_title.move_to(LEFT*3.2 + UP*2.0)
        right_title.move_to(RIGHT*3.2 + UP*2.0)

        arr_decl2 = code_text("int marks[5];", size=24)
        arr_decl2.next_to(left_title, DOWN, buff=0.2)

        arr_mem2 = VGroup(*[
            memory_block("", 1000 + 4*i, width=1.0, height=0.75) for i in range(5)
        ]).arrange(RIGHT, buff=0)
        arr_mem2.scale(0.85)
        arr_mem2.next_to(arr_decl2, DOWN, buff=0.35)

        arr_desc = VGroup(
            small_text("Actual block of 5 integers", size=20),
            small_text("Memory for all elements exists here", size=20),
            small_text("Fixed-size collection", size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        arr_desc.next_to(arr_mem2, DOWN, buff=0.25)

        ptr_decl = code_text("int *p;", size=24)
        ptr_decl.next_to(right_title, DOWN, buff=0.2)

        ptr_var = pointer_box("p", "1000", width=2.2, height=0.9)
        ptr_var.next_to(ptr_decl, DOWN, buff=0.35)

        ptr_target = VGroup(*[
            memory_block("", 1000 + 4*i, width=1.0, height=0.75) for i in range(3)
        ]).arrange(RIGHT, buff=0)
        ptr_target.scale(0.85)
        ptr_target.next_to(ptr_var, DOWN, buff=0.45)

        ptr_arrow = Arrow(ptr_var.get_bottom(),
                          ptr_target[0].get_top(), buff=0.1, stroke_color=BLUE)

        ptr_desc = VGroup(
            small_text("Separate variable storing an address", size=20),
            small_text("Can point somewhere else later", size=20),
            small_text("Does not itself contain all array elements", size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ptr_desc.next_to(ptr_target, DOWN, buff=0.25)

        self.play(FadeIn(divider), FadeIn(left_title),
                  FadeIn(right_title), run_time=0.8)
        self.play(
            FadeIn(arr_decl2), FadeIn(arr_mem2), FadeIn(arr_desc),
            FadeIn(ptr_decl), FadeIn(ptr_var), FadeIn(ptr_target),
            run_time=1.0
        )
        self.play(GrowArrow(ptr_arrow), FadeIn(ptr_desc), run_time=0.8)

        diff1 = body_text("So an array is not a pointer.",
                          size=26, color=PRIMARY_HIGHLIGHT)
        diff1.to_edge(DOWN).shift(UP*0.45)
        self.play(Write(diff1), run_time=0.7)

        diff2 = body_text(
            "But in many expressions, the array name behaves like the address of the first element.", size=22)
        diff2.next_to(diff1, UP, buff=0.14)
        self.play(FadeIn(diff2), run_time=0.8)
        self.wait(1.8)

        self.play(
            FadeOut(divider), FadeOut(left_title), FadeOut(right_title),
            FadeOut(arr_decl2), FadeOut(arr_mem2), FadeOut(arr_desc),
            FadeOut(ptr_decl), FadeOut(ptr_var), FadeOut(ptr_target),
            FadeOut(ptr_arrow), FadeOut(ptr_desc),
            FadeOut(diff1), FadeOut(diff2), FadeOut(t8),
            run_time=0.9
        )

        # -------------------------------------------------
        # 9. Why array feels pointer-like in C
        # -------------------------------------------------
        t9 = title_text(
            "Then why does an array feel pointer-like in C?", size=31)
        t9.next_to(header, DOWN, buff=0.55)
        self.play(Write(t9), run_time=0.8)

        code_grp = VGroup(
            code_text("int marks[5] = {78, 85, 91, 67, 88};", size=24),
            code_text("*marks        // 78", size=24, color=BLUE),
            code_text("*(marks + 3)  // 67", size=24, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_grp.move_to(ORIGIN + UP*0.2)

        self.play(FadeIn(code_grp), run_time=0.9)

        expl = VGroup(
            body_text(
                "Because the array name can decay to a pointer to its first element.", size=23),
            body_text("But the array itself is still the whole contiguous block.",
                      size=23, color=PRIMARY_HIGHLIGHT)
        ).arrange(DOWN, buff=0.14)
        expl.next_to(code_grp, DOWN, buff=0.35)

        self.play(FadeIn(expl), run_time=0.8)

        func = VGroup(
            body_text("Common C function behavior:",
                      size=24, color=PRIMARY_HIGHLIGHT),
            code_text("void printArray(int arr[], int n)", size=24),
            body_text(
                "Inside the parameter list, this behaves like int *arr", size=22)
        ).arrange(DOWN, buff=0.14)
        func.to_edge(DOWN).shift(UP*0.45)

        self.play(FadeIn(func), run_time=0.9)
        self.wait(1.7)

        self.play(FadeOut(t9), FadeOut(code_grp), FadeOut(
            expl), FadeOut(func), run_time=0.8)

        # -------------------------------------------------
        # 10. Dimensions of arrays
        # -------------------------------------------------
        t10 = title_text(
            "Arrays can have one, two, or more dimensions", size=31)
        t10.next_to(header, DOWN, buff=0.55)
        self.play(Write(t10), run_time=0.8)

        one_d_title = body_text("1D Array", size=25, color=PRIMARY_HIGHLIGHT)
        one_d_title.move_to(LEFT*4 + UP*1.8)

        one_d = VGroup(*[array_block(v, i, width=0.95, height=0.75)
                       for i, v in enumerate([2, 4, 6, 8])])
        one_d.arrange(RIGHT, buff=0)
        one_d.next_to(one_d_title, DOWN, buff=0.25)

        one_d_code = code_text("int a[4];", size=22)
        one_d_code.next_to(one_d, DOWN, buff=0.2)

        two_d_title = body_text("2D Array", size=25, color=PRIMARY_HIGHLIGHT)
        two_d_title.move_to(ORIGIN + UP*1.8)

        grid_2d = VGroup()
        vals_2d = [[1, 2], [3, 4], [5, 6]]
        for row in vals_2d:
            row_group = VGroup(*[array_block(v, width=0.82, height=0.68)
                               for v in row]).arrange(RIGHT, buff=0)
            grid_2d.add(row_group)
        grid_2d.arrange(DOWN, buff=0)
        grid_2d.next_to(two_d_title, DOWN, buff=0.25)

        two_d_code = code_text("int m[3][2];", size=22)
        two_d_code.next_to(grid_2d, DOWN, buff=0.2)

        three_d_title = body_text("3D Array", size=25, color=PRIMARY_HIGHLIGHT)
        three_d_title.move_to(RIGHT*4 + UP*1.8)

        front = VGroup(*[array_block(v, width=0.72, height=0.6)
                       for v in [1, 2, 3, 4]]).arrange_in_grid(rows=2, cols=2, buff=0)
        back = VGroup(*[array_block(v, width=0.72, height=0.6)
                      for v in [5, 6, 7, 8]]).arrange_in_grid(rows=2, cols=2, buff=0)

        back.shift(RIGHT*0.22 + UP*0.22)
        cube = VGroup(back, front)
        cube.next_to(three_d_title, DOWN, buff=0.3)

        three_d_code = code_text("int box[2][2][2];", size=22)
        three_d_code.next_to(cube, DOWN, buff=0.2)

        self.play(
            FadeIn(one_d_title), FadeIn(one_d), FadeIn(one_d_code),
            FadeIn(two_d_title), FadeIn(grid_2d), FadeIn(two_d_code),
            FadeIn(three_d_title), FadeIn(cube), FadeIn(three_d_code),
            run_time=1.3
        )

        dim_note = body_text(
            "1D stores a list, 2D stores a table, 3D stores layered data.",
            size=24,
            color=PRIMARY_HIGHLIGHT
        )
        dim_note.to_edge(DOWN).shift(UP*0.4)
        self.play(FadeIn(dim_note), run_time=0.7)
        self.wait(1.7)

        self.play(
            FadeOut(t10),
            FadeOut(one_d_title), FadeOut(one_d), FadeOut(one_d_code),
            FadeOut(two_d_title), FadeOut(grid_2d), FadeOut(two_d_code),
            FadeOut(three_d_title), FadeOut(cube), FadeOut(three_d_code),
            FadeOut(dim_note),
            run_time=0.9
        )

        # -------------------------------------------------
        # 11. Applications
        # -------------------------------------------------
        t11 = title_text("Where are arrays used?", size=32)
        t11.next_to(header, DOWN, buff=0.55)
        self.play(Write(t11), run_time=0.8)

        app1 = panel(["Marks", "Temperatures"], width=3.7, height=1.8,
                     fill=SECONDARY_ACCENT, stroke=PRIMARY_HIGHLIGHT)
        app2 = panel(["Matrix data", "Image pixels"], width=3.7,
                     height=1.8, fill="#dcfce7", stroke=GREEN)
        app3 = panel(["Sensor readings", "Daily sales"], width=3.7,
                     height=1.8, fill="#dbeafe", stroke=BLUE)

        apps = VGroup(app1, app2, app3).arrange(RIGHT, buff=0.3)
        apps.scale(0.92)
        apps.move_to(ORIGIN + DOWN*0.1)

        self.play(LaggedStart(*[FadeIn(a, shift=UP*0.1)
                  for a in apps], lag_ratio=0.15), run_time=1.0)

        app_note = body_text(
            "Use arrays when you have many similar values and want indexed access.",
            size=24,
            color=PRIMARY_HIGHLIGHT
        )
        app_note.to_edge(DOWN).shift(UP*0.4)
        self.play(FadeIn(app_note), run_time=0.7)
        self.wait(1.4)

        self.play(FadeOut(t11), FadeOut(apps), FadeOut(app_note), run_time=0.8)

        # -------------------------------------------------
        # 12. Final definition
        # -------------------------------------------------
        t12 = title_text("Definition", size=34, color=PRIMARY_HIGHLIGHT)
        t12.next_to(header, DOWN, buff=0.55)
        self.play(Write(t12), run_time=0.8)

        def_box = RoundedRectangle(
            corner_radius=0.18,
            width=10.2,
            height=4.0,
            stroke_color=PRIMARY_HIGHLIGHT,
            stroke_width=2,
            fill_color=SECONDARY_ACCENT,
            fill_opacity=0.6
        )

        definition = Paragraph(
            "An array is a linear data structure that stores multiple\n"
            "elements of the same data type in contiguous memory\n"
            "locations, and each element is accessed using an index.\n"
            "Arrays can also be one-dimensional, two-dimensional,\n"
            "three-dimensional, and beyond.",
            alignment="center",
            font_size=28,
            color=TEXT_COLOR,
            line_spacing=0.9
        )

        final_group = VGroup(def_box, definition)
        final_group.move_to(ORIGIN + DOWN*0.1)

        self.play(FadeIn(def_box), Write(definition), run_time=1.3)
        self.wait(2.0)

        self.play(FadeOut(t12), FadeOut(final_group), run_time=0.8)

        # -------------------------------------------------
        # 13. Final takeaway
        # -------------------------------------------------
        takeaway = VGroup(
            title_text("What should you remember?", size=32),
            body_text(
                "• Arrays store many same-type values under one name", size=24),
            body_text("• They use contiguous memory", size=24),
            body_text(
                "• They support indexed access and easy traversal", size=24),
            body_text("• In C, array names can act pointer-like", size=24),
            body_text("• But an array itself is not a pointer",
                      size=24, color=PRIMARY_HIGHLIGHT),
            body_text("• Arrays may be 1D, 2D, 3D, and more", size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        takeaway.move_to(ORIGIN)
        self.play(FadeIn(takeaway, shift=UP*0.12), run_time=1.0)
        self.wait(2.5)
