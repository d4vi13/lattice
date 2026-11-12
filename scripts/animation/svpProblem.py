from manim import *
import numpy as np


def generateLatticeGrid(b1, b2, gridRange=8):
    points = []
    for i in range(-gridRange, gridRange + 1):
        for j in range(-gridRange, gridRange + 1):
            pt = i * b1 + j * b2
            if abs(pt[0]) <= 7.2 and abs(pt[1]) <= 4.2:
                points.append(pt)
    return points


def findShortestVector(latticeCoords):
    nonZeroCoords = [pt for pt in latticeCoords if np.linalg.norm(pt) > 1e-6]
    # Prioriza o representante no semiplano direito (x > 0) em caso de empate simétrico (+v e -v)
    shortestPt = min(
        nonZeroCoords,
        key=lambda pt: (round(float(np.linalg.norm(pt)), 6), -pt[0]),
    )
    minNorm = float(np.linalg.norm(shortestPt))
    return shortestPt, minNorm


class svpAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        # Base não-reduzida (vetores longos e inclinados que geram o reticulado)
        b1 = np.array([2.2, 2.3, 0.0])
        b2 = np.array([1.0, 2.0, 0.0])

        # 1. Introdução
        titleText = Text(
            "SVP: Shortest Vector Problem", font_size=36, color=WHITE
        ).to_edge(UP, buff=0.4)
        subtitleText = MathTex(
            r"\text{Dado uma base } B, \text{ encontrar } \mathbf{v} \in \mathcal{L}(B) \setminus \{\mathbf{0}\} \text{ minimizando } \|\mathbf{v}\|_2",
            font_size=26,
            color="#94a3b8",
        ).next_to(titleText, DOWN, buff=0.2)

        self.play(Write(titleText), FadeIn(subtitleText), run_time=2.0)
        self.wait(1.2)

        # 2. Construção do Espaço (reticulado e origem)
        latticeCoords = generateLatticeGrid(b1, b2, gridRange=8)
        latticeDots = VGroup(
            *[Dot(point=pt, radius=0.07, color="#64748b") for pt in latticeCoords]
        )
        originDot = Dot(point=ORIGIN, radius=0.09, color=WHITE)
        originLabel = MathTex(r"\mathbf{0}", color=WHITE, font_size=26).next_to(
            originDot, DOWN + LEFT, buff=0.12
        )

        self.play(FadeIn(latticeDots, lag_ratio=0.025), run_time=2.2)
        self.play(FadeIn(originDot), Write(originLabel), run_time=0.9)
        self.wait(1.0)

        # 3. Apresentação do Problema (vetores da base inseridos sequencialmente)
        vecB1 = Arrow(ORIGIN, b1, buff=0, color="#38bdf8", stroke_width=4)
        labelB1 = MathTex(r"\mathbf{b}_1", color="#38bdf8", font_size=28).next_to(
            vecB1.get_end(), RIGHT, buff=0.14
        )
        self.play(GrowArrow(vecB1), Write(labelB1), run_time=1.5)
        self.wait(0.5)

        vecB2 = Arrow(ORIGIN, b2, buff=0, color="#818cf8", stroke_width=4)
        labelB2 = MathTex(r"\mathbf{b}_2", color="#818cf8", font_size=28).next_to(
            vecB2.get_end(), LEFT, buff=0.14
        )
        self.play(GrowArrow(vecB2), Write(labelB2), run_time=1.5)
        self.wait(1.5)

        # 4. Dinâmica de Busca (bola euclidiana expandindo a partir da origem)
        shortestPt, minNorm = findShortestVector(latticeCoords)

        expandCircle = Circle(
            radius=0.05,
            color="#f43f5e",
            stroke_width=2.5,
            fill_color="#f43f5e",
            fill_opacity=0.1,
        ).move_to(ORIGIN)
        radiusTracker = ValueTracker(0.05)
        expandCircle.add_updater(
            lambda mob: mob.become(
                Circle(
                    radius=radiusTracker.get_value(),
                    color="#f43f5e",
                    stroke_width=2.5,
                    fill_color="#f43f5e",
                    fill_opacity=0.1,
                ).move_to(ORIGIN)
            )
        )

        self.play(Create(expandCircle), run_time=0.8)
        self.play(
            radiusTracker.animate.set_value(minNorm),
            run_time=4.2,
            rate_func=smooth,
        )
        expandCircle.clear_updaters()
        self.wait(1.0)

        # 5. Conclusão Visual (vetor não-nulo mais curto v = b1 - b2)
        shortestDot = Dot(point=shortestPt, radius=0.11, color="#10b981")
        vecV = Arrow(ORIGIN, shortestPt, buff=0, color="#10b981", stroke_width=5)
        labelV = MathTex(
            r"\mathbf{v} = \mathbf{b}_1 - \mathbf{b}_2",
            color="#10b981",
            font_size=28,
        ).next_to(shortestDot, DOWN + RIGHT, buff=0.14)

        unitV = shortestPt / minNorm
        normalVec = np.array([-unitV[1], unitV[0], 0.0])
        offsetVec = normalVec * 0.26

        normLine = DashedLine(
            ORIGIN + offsetVec,
            shortestPt + offsetVec,
            color="#fbbf24",
            stroke_width=4,
            dash_length=0.1,
        )
        normLabel = MathTex(
            r"\lambda_1(\mathcal{L}) = \min \|\mathbf{v}\|_2",
            color="#fbbf24",
            font_size=26,
        ).next_to(normLine.get_center(), UP + LEFT, buff=0.14)

        self.play(
            FadeIn(shortestDot),
            GrowArrow(vecV),
            Write(labelV),
            run_time=1.8,
        )
        self.play(Create(normLine), Write(normLabel), run_time=1.6)
        self.play(
            Indicate(shortestDot, scale_factor=1.35),
            Indicate(vecV, scale_factor=1.08),
            run_time=1.5,
        )
        self.wait(3.0)


class svpThumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        b1 = np.array([2.2, 2.3, 0.0])
        b2 = np.array([1.0, 2.0, 0.0])

        latticeCoords = generateLatticeGrid(b1, b2, gridRange=8)
        latticeDots = VGroup(
            *[Dot(point=pt, radius=0.08, color="#475569") for pt in latticeCoords]
        )

        shortestPt, minNorm = findShortestVector(latticeCoords)

        # Esfera de norma mínima centrada na origem
        normCircle = Circle(
            radius=minNorm,
            color="#f43f5e",
            stroke_width=5,
            fill_color="#f43f5e",
            fill_opacity=0.15,
        ).move_to(ORIGIN)

        # Vetores da base (em segundo plano visual) e solução ótima
        vecB1 = Arrow(ORIGIN, b1, buff=0, color="#38bdf8", stroke_width=5)
        vecB2 = Arrow(ORIGIN, b2, buff=0, color="#818cf8", stroke_width=5)
        vecV = Arrow(ORIGIN, shortestPt, buff=0, color="#10b981", stroke_width=7)

        unitV = shortestPt / minNorm
        normalVec = np.array([-unitV[1], unitV[0], 0.0])
        offsetVec = normalVec * 0.28
        normLine = DashedLine(
            ORIGIN + offsetVec,
            shortestPt + offsetVec,
            color="#fbbf24",
            stroke_width=5,
            dash_length=0.12,
        )

        originDot = Dot(ORIGIN, radius=0.11, color=WHITE)
        shortestDot = Dot(shortestPt, radius=0.13, color="#10b981")

        labelOrigin = MathTex(r"\mathbf{0}", font_size=38, color=WHITE).next_to(
            originDot, DOWN + LEFT, buff=0.12
        )
        labelB1 = MathTex(r"\mathbf{b}_1", font_size=38, color="#38bdf8").next_to(
            vecB1.get_end(), RIGHT, buff=0.14
        )
        labelB2 = MathTex(r"\mathbf{b}_2", font_size=38, color="#818cf8").next_to(
            vecB2.get_end(), LEFT, buff=0.14
        )
        labelV = MathTex(r"\mathbf{v}", font_size=44, color="#10b981").next_to(
            shortestDot, DOWN + RIGHT, buff=0.12
        )

        # Banner superior para leitura imediata na thumbnail
        bannerBg = Rectangle(
            width=14.2,
            height=1.6,
            fill_color="#020617",
            fill_opacity=0.85,
            stroke_width=0,
        ).to_edge(UP, buff=0)
        title = Text("SVP", font_size=64, weight=BOLD, color="#f43f5e").move_to(
            bannerBg.get_left() + RIGHT * 1.3
        )
        subtitle = Text(
            "Shortest Vector Problem", font_size=38, weight=BOLD, color=WHITE
        ).next_to(title, RIGHT, buff=0.35)
        formula = MathTex(
            r"\min_{\mathbf{v} \neq \mathbf{0}} \|\mathbf{v}\|_2",
            font_size=44,
            color="#fbbf24",
        ).move_to(bannerBg.get_right() + LEFT * 2.0)

        self.add(
            latticeDots,
            normCircle,
            vecB1,
            vecB2,
            vecV,
            normLine,
            originDot,
            shortestDot,
            labelOrigin,
            labelB1,
            labelB2,
            labelV,
            bannerBg,
            title,
            subtitle,
            formula,
        )
