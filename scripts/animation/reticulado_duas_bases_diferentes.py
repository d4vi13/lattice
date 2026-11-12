from manim import *
import numpy as np

# Configure Manim to save directly without auto-playing
config.preview = False
config.quality = "high_quality"


def build_lattice_elements():
    """Creates shared geometry for both the animation and the static thumbnail."""
    plano = NumberPlane(
        x_range=[-8, 8, 1],
        y_range=[-5, 5, 1],
        background_line_style={
            "stroke_color": GREY_D,
            "stroke_width": 1,
            "stroke_opacity": 0.4,
        },
    )

    # Base 1 (Boa / Curta)
    b1 = np.array([1.2, 0.2, 0.0])
    b2 = np.array([0.3, 1.1, 0.0])

    # Transformação Unimodular U = [[2, 1], [1, 1]] (det(U) = 1)
    # Base 2 (Ruim / Alongada)
    c1 = 2 * b1 + 1 * b2  # (2.7, 1.5)
    c2 = 1 * b1 + 1 * b2  # (1.5, 1.3)

    # Pontos do reticulado
    pontos = VGroup()
    for i in range(-12, 13):
        for j in range(-12, 13):
            pos = i * b1 + j * b2
            if abs(pos[0]) <= 7.2 and abs(pos[1]) <= 4.1:
                pontos.add(Dot(point=pos, radius=0.06, color=WHITE))

    # Vetores e rótulos da Base 1
    vec_b1 = Arrow(ORIGIN, b1, buff=0, color=BLUE, stroke_width=5)
    vec_b2 = Arrow(ORIGIN, b2, buff=0, color=GREEN, stroke_width=5)
    label_b1 = MathTex(r"\mathbf{b}_1", color=BLUE).next_to(
        vec_b1.get_end(), DOWN, buff=0.15
    )
    label_b2 = MathTex(r"\mathbf{b}_2", color=GREEN).next_to(
        vec_b2.get_end(), LEFT, buff=0.15
    )

    paralelogramo_1 = Polygon(
        ORIGIN,
        b1,
        b1 + b2,
        b2,
        color=BLUE_B,
        fill_color=BLUE,
        fill_opacity=0.25,
        stroke_width=2,
    )

    # Vetores e rótulos da Base 2
    vec_c1 = Arrow(ORIGIN, c1, buff=0, color=RED, stroke_width=5)
    vec_c2 = Arrow(ORIGIN, c2, buff=0, color=ORANGE, stroke_width=5)
    label_c1 = MathTex(r"\mathbf{c}_1", color=RED).next_to(
        vec_c1.get_end(), RIGHT, buff=0.15
    )
    label_c2 = MathTex(r"\mathbf{c}_2", color=ORANGE).next_to(
        vec_c2.get_end(), UP, buff=0.15
    )

    paralelogramo_2 = Polygon(
        ORIGIN,
        c1,
        c1 + c2,
        c2,
        color=ORANGE,
        fill_color=RED,
        fill_opacity=0.25,
        stroke_width=2,
    )

    # Malha estendida da Base 2
    linhas_c1 = VGroup()
    linhas_c2 = VGroup()
    for k in range(-18, 19):
        linhas_c1.add(
            Line(
                k * c2 - 12 * c1,
                k * c2 + 12 * c1,
                color=RED_E,
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
        )
        linhas_c2.add(
            Line(
                k * c1 - 12 * c2,
                k * c1 + 12 * c2,
                color=ORANGE,
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
        )

    return {
        "plano": plano,
        "b1": b1,
        "b2": b2,
        "pontos": pontos,
        "vec_b1": vec_b1,
        "vec_b2": vec_b2,
        "label_b1": label_b1,
        "label_b2": label_b2,
        "paralelogramo_1": paralelogramo_1,
        "vec_c1": vec_c1,
        "vec_c2": vec_c2,
        "label_c1": label_c1,
        "label_c2": label_c2,
        "paralelogramo_2": paralelogramo_2,
        "linhas_c1": linhas_c1,
        "linhas_c2": linhas_c2,
    }


class ReticuladoDuasBases(Scene):

    def construct(self):
        el = build_lattice_elements()
        self.play(Create(el["plano"]), run_time=0.6)

        info_b1 = (
            MathTex(
                r"\mathcal{B}_1 = \{\mathbf{b}_1, \mathbf{b}_2\}",
                r"\implies \Lambda = \{m\mathbf{b}_1 + n\mathbf{b}_2 \mid m, n \in \mathbb{Z}\}",
                font_size=28,
            )
            .to_edge(DOWN)
            .add_background_rectangle(opacity=0.85, buff=0.15)
        )

        self.play(
            GrowArrow(el["vec_b1"]),
            Write(el["label_b1"]),
            GrowArrow(el["vec_b2"]),
            Write(el["label_b2"]),
            run_time=0.7,
        )
        self.play(FadeIn(el["paralelogramo_1"]), Write(info_b1), run_time=0.7)

        b1, b2 = el["b1"], el["b2"]
        comb_ex = DashedLine(b1, b1 + b2, color=GREEN_A)
        comb_ex2 = DashedLine(b2, b1 + b2, color=BLUE_A)
        self.play(Create(comb_ex), Create(comb_ex2), run_time=0.4)
        self.play(FadeIn(el["pontos"], lag_ratio=0.01), run_time=1.2)
        self.play(FadeOut(comb_ex), FadeOut(comb_ex2), run_time=0.3)
        self.wait(0.8)

        info_transicao = (
            MathTex(
                r"\mathbf{c}_1 = 2\mathbf{b}_1 + \mathbf{b}_2, \quad \mathbf{c}_2 = \mathbf{b}_1 + \mathbf{b}_2",
                r"\quad (\det U = 1)",
                font_size=28,
                color=YELLOW,
            )
            .to_edge(DOWN)
            .add_background_rectangle(opacity=0.85, buff=0.15)
        )

        self.play(FadeOut(info_b1), FadeIn(info_transicao), run_time=0.5)
        self.wait(0.5)

        self.play(
            GrowArrow(el["vec_c1"]),
            Write(el["label_c1"]),
            GrowArrow(el["vec_c2"]),
            Write(el["label_c2"]),
            run_time=0.7,
        )
        self.wait(0.3)

        self.play(
            FadeOut(el["vec_b1"]),
            FadeOut(el["label_b1"]),
            FadeOut(el["vec_b2"]),
            FadeOut(el["label_b2"]),
            ReplacementTransform(el["paralelogramo_1"], el["paralelogramo_2"]),
            run_time=0.8,
        )

        info_b2 = (
            MathTex(
                r"\mathcal{B}_2 = \{\mathbf{c}_1, \mathbf{c}_2\}",
                r"\implies \Lambda = \{p\mathbf{c}_1 + q\mathbf{c}_2 \mid p, q \in \mathbb{Z}\}",
                font_size=28,
            )
            .to_edge(DOWN)
            .add_background_rectangle(opacity=0.85, buff=0.15)
        )

        self.play(FadeOut(info_transicao), FadeIn(info_b2), run_time=0.5)

        self.bring_to_front(
            el["pontos"],
            el["paralelogramo_2"],
            el["vec_c1"],
            el["vec_c2"],
            el["label_c1"],
            el["label_c2"],
            info_b2,
        )
        self.play(
            Create(el["linhas_c1"]), Create(el["linhas_c2"]), run_time=1.0
        )
        self.wait(1.5)


class ReticuladoThumbnail(Scene):
    """Static thumbnail showing BOTH bases and fundamental regions simultaneously."""

    def construct(self):
        el = build_lattice_elements()

        # Subtle grid lines in the background
        el["linhas_c1"].set_stroke(opacity=0.35)
        el["linhas_c2"].set_stroke(opacity=0.35)

        # Clean visual comparison equation at the bottom
        legenda = (
            MathTex(
                r"\Lambda(\mathcal{B}_1) = \Lambda(\mathcal{B}_2)",
                font_size=36,
            )
            .to_edge(DOWN, buff=0.35)
            .add_background_rectangle(opacity=0.88, buff=0.18)
        )

        # Add layers in back-to-front order (no self.play -> renders single frame)
        self.add(
            el["plano"],
            el["linhas_c1"],
            el["linhas_c2"],
            el["paralelogramo_2"],
            el["paralelogramo_1"],
            el["pontos"],
            el["vec_c1"],
            el["vec_c2"],
            el["label_c1"],
            el["label_c2"],
            el["vec_b1"],
            el["vec_b2"],
            el["label_b1"],
            el["label_b2"],
            legenda,
        )
