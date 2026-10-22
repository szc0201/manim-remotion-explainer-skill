import numpy as np
from manim import *


class FormulaDemo(Scene):
    def construct(self):
        self.camera.background_opacity = 0
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-1.1, 1.1, 0.5],
            x_length=6.6,
            y_length=2.4,
            tips=False,
            axis_config={"color": "#91AABD", "stroke_width": 1.4},
        ).move_to(UP * 0.7)
        curve = axes.plot(
            lambda t: np.sin(TAU * 2 * t),
            x_range=[0, 1, 0.002],
            color="#53DCFF",
        )
        curve.set_stroke(width=3.4)
        formula = MathTex(
            r"y(t)=\sin(2\pi f t)",
            r"\qquad f=2\,\mathrm{Hz}",
            font_size=42,
        )
        formula[0].set_color("#F4F8FB")
        formula[1].set_color("#FF9B51")
        formula.move_to(UP * 2.65)
        time_label = Text("TIME DOMAIN", font_size=20, color="#91AABD")
        time_label.next_to(axes, DOWN, buff=0.3)

        self.play(Create(axes), run_time=1.2)
        self.play(Create(curve), run_time=1.2)
        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(time_label), run_time=0.5)
        self.wait(1.0)
        self.play(Indicate(formula[1], color="#53DCFF"), run_time=0.5)
        self.wait(0.8)
