from manim import *
import numpy as np


def generateLatticeGrid(b1, b2, gridRange=7):
    points = []
    for i in range(-gridRange, gridRange + 1):
        for j in range(-gridRange, gridRange + 1):
            pt = i * b1 + j * b2
            if abs(pt[0]) <= 7.2 and abs(pt[1]) <= 4.2:
                points.append(pt)
    return points


class cvpAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        # Base moderadamente inclinada
        b1 = np.array([1.8, 0.3, 0.0])
        b2 = np.array([0.7, 1.5, 0.0])

        titleText = Text(
            "CVP: Closest Vector Problem", font_size=36, color=WHITE
        ).to_edge(UP, buff=0.4)
        subtitleText = MathTex(
            r"\text{Dado } \mathbf{t} \in \mathbb{R}^n, \text{ encontrar } \mathbf{v} \in \mathcal{L}(B) \text{ minimizando } \|\mathbf{t} - \mathbf{v}\|_2",
            font_size=26,
            color="#94a3b8",
        ).next_to(titleText, DOWN, buff=0.2)

        self.play(Write(titleText), FadeIn(subtitleText))

        latticeCoords = generateLatticeGrid(b1, b2, gridRange=8)
        dots = VGroup(
            *[Dot(point=pt, radius=0.07, color="#64748b") for pt in latticeCoords]
        )
        self.play(FadeIn(dots, lag_ratio=0.01))

        # Vetores da base na origem
        vecB1 = Arrow(ORIGIN, b1, buff=0, color="#38bdf8", stroke_width=4)
        vecB2 = Arrow(ORIGIN, b2, buff=0, color="#818cf8", stroke_width=4)
        labelB1 = MathTex(r"\mathbf{b}_1", color="#38bdf8", font_size=26).next_to(
            vecB1.get_end(), DOWN, buff=0.1
        )
        labelB2 = MathTex(r"\mathbf{b}_2", color="#818cf8", font_size=26).next_to(
            vecB2.get_end(), LEFT, buff=0.1
        )
        self.play(GrowArrow(vecB1), GrowArrow(vecB2), Write(labelB1), Write(labelB2))

        # Ponto alvo t fora do reticulado
        targetPt = np.array([3.1, 2.2, 0.0])
        targetDot = Dot(point=targetPt, radius=0.11, color="#f43f5e")
        targetCross = Cross(scale_factor=0.15, color="#f43f5e").move_to(targetPt)
        targetLabel = MathTex(
            r"\mathbf{t} \notin \mathcal{L}", color="#f43f5e", font_size=30
        ).next_to(targetDot, UP + RIGHT, buff=0.12)

        self.play(FadeIn(targetDot), Create(targetCross), Write(targetLabel))
        self.wait(0.6)

        # Encontrar o ponto mais próximo exato entre os gerados
        closestPt = min(latticeCoords, key=lambda p: np.linalg.norm(p - targetPt))
        minDist = np.linalg.norm(closestPt - targetPt)

        # Esfera expandindo a partir de t até tocar o primeiro ponto do reticulado
        expandCircle = Circle(radius=0.05, color="#f43f5e").move_to(targetPt)
        radiusTracker = ValueTracker(0.05)
        expandCircle.add_updater(
            lambda m: m.become(
                Circle(
                    radius=radiusTracker.get_value(),
                    color="#f43f5e",
                    stroke_width=2.5,
                    fill_color="#f43f5e",
                    fill_opacity=0.1,
                ).move_to(targetPt)
            )
        )

        self.play(Create(expandCircle))
        self.play(
            radiusTracker.animate.set_value(minDist),
            run_time=2.2,
            rate_func=smooth,
        )
        expandCircle.clear_updaters()

        # Destacar o vetor solução v e o vetor de erro e = t - v
        closestDot = Dot(point=closestPt, radius=0.11, color="#10b981")
        vecV = Arrow(ORIGIN, closestPt, buff=0, color="#10b981", stroke_width=5)
        labelV = MathTex(
            r"\mathbf{v} \in \mathcal{L}", color="#10b981", font_size=28
        ).next_to(closestDot, DOWN + RIGHT, buff=0.12)

        errorLine = DashedLine(
            closestPt, targetPt, color="#fbbf24", stroke_width=4, dash_length=0.1
        )
        errorLabel = MathTex(
            r"\min \|\mathbf{t} - \mathbf{v}\|_2", color="#fbbf24", font_size=26
        ).next_to(errorLine.get_center(), LEFT, buff=0.2)

        self.play(
            FadeIn(closestDot),
            GrowArrow(vecV),
            Write(labelV),
            Create(errorLine),
            Write(errorLabel),
        )
        self.play(Indicate(closestDot, scale_factor=1.4))
        self.wait(2)


class cvpThumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        b1 = np.array([1.8, 0.3, 0.0])
        b2 = np.array([0.7, 1.5, 0.0])

        coords = generateLatticeGrid(b1, b2, gridRange=8)
        dots = VGroup(*[Dot(point=pt, radius=0.08, color="#475569") for pt in coords])

        targetPt = np.array([2.9, 1.9, 0.0])
        closestPt = min(coords, key=lambda p: np.linalg.norm(p - targetPt))
        minDist = np.linalg.norm(closestPt - targetPt)

        # Círculo de busca centrado em t
        distCircle = Circle(
            radius=minDist,
            color="#f43f5e",
            stroke_width=4,
            fill_color="#f43f5e",
            fill_opacity=0.15,
        ).move_to(targetPt)

        vecV = Arrow(ORIGIN, closestPt, buff=0, color="#10b981", stroke_width=7)
        errorLine = DashedLine(closestPt, targetPt, color="#fbbf24", stroke_width=5)

        originDot = Dot(ORIGIN, radius=0.1, color=WHITE)
        closestDot = Dot(closestPt, radius=0.13, color="#10b981")
        targetDot = Dot(targetPt, radius=0.13, color="#f43f5e")

        labelT = MathTex(r"\mathbf{t}", font_size=42, color="#f43f5e").next_to(
            targetDot, UP + RIGHT, buff=0.1
        )
        labelV = MathTex(r"\mathbf{v}", font_size=42, color="#10b981").next_to(
            closestDot, DOWN + RIGHT, buff=0.1
        )

        # Banner superior para leitura imediata na thumbnail
        bannerBg = Rectangle(
            width=14.2, height=1.6, fill_color="#020617", fill_opacity=0.85, stroke_width=0
        ).to_edge(UP, buff=0)
        title = Text("CVP", font_size=64, weight=BOLD, color="#f43f5e").move_to(
            bannerBg.get_left() + RIGHT * 1.5
        )
        subtitle = Text(
            "Closest Vector Problem", font_size=38, weight=BOLD, color=WHITE
        ).next_to(title, RIGHT, buff=0.4)
        formula = MathTex(
            r"\min \|\mathbf{t} - \mathbf{v}\|_2", font_size=44, color="#fbbf24"
        ).move_to(bannerBg.get_right() + LEFT * 2.1)

        self.add(
            dots,
            distCircle,
            vecV,
            errorLine,
            originDot,
            closestDot,
            targetDot,
            labelT,
            labelV,
            bannerBg,
            title,
            subtitle,
            formula,
        )
