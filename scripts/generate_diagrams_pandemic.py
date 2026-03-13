#!/usr/bin/env python3
"""
PresentationBanana — Pandemic/Infodemic Diagram Generator
==========================================================
Generates all Excalidraw diagrams for the pandemic-infodemic presentation.
Slides: 2, 4, 6, 7, 9, 11, 12, 14, 15, 16, 17
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_excalidraw import ExcalidrawBuilder

# ── Constants ────────────────────────────────────────────────────────────────
OUT_DIR = Path(__file__).parent.parent / "output" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)
SLUG = "pandemic-infodemic"

C_GOLD   = "#F0AB00"
C_BLUE   = "#4A9EE0"
C_TEAL   = "#2EA89D"
C_GREEN  = "#3EB489"
C_PURPLE = "#9B6DD0"
C_ORANGE = "#E8853D"
C_RED    = "#E04B4B"
C_BOX    = "#1E3050"
C_WHITE  = "#FFFFFF"
C_LIGHT  = "#C8D6E5"
C_MUTED  = "#7A8BA0"
C_BG     = "#121A2E"


def export(eb, slide_num):
    path = OUT_DIR / f"{SLUG}_s{slide_num:02d}_diagram.png"
    try:
        result = eb.export_png(str(path), scale=2)
        print(f"  S{slide_num:02d}: {result}")
        return result
    except Exception as e:
        print(f"  S{slide_num:02d} ERROR: {e}")
        return None


# ── Slide 2: Roadmap Flow (4 Acts) ──────────────────────────────────────────

def slide_02_roadmap():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 480, 30, color=C_GOLD, width=3)

    # 4 boxes horizontally
    bw, bh = 240, 160
    gap = 40
    start_x = (W - 4 * bw - 3 * gap) // 2
    y = (H - bh) // 2 + 20

    boxes = [
        ("Act 1", "Infodemic Analogy\n& Its Limits", C_RED),
        ("Act 2", "CET Framework\nIntroduced", C_BLUE),
        ("Act 3", "Biases + TRIMs\nMechanisms", C_TEAL),
        ("Act 4", "Prebunking\nSolution", C_GREEN),
    ]

    for i, (act, label, color) in enumerate(boxes):
        x = start_x + i * (bw + gap)
        bname = f"box{i}"
        eb.rect(x, y, bw, bh, fill=C_BOX, stroke=color, name=bname)
        eb.text(x + 10, y + 12, act, size=16, color=color, font_family=5)
        eb.line(x + 10, y + 38, x + bw - 20, y + 38, color=color, width=1)
        eb.text(x + 10, y + 50, label, size=20, color=C_WHITE, font_family=5)

        # Arrow between boxes (not after last)
        if i < 3:
            ax1 = x + bw
            ax2 = x + bw + gap
            ay = y + bh // 2
            eb.arrow(ax1, ay, ax2, ay, color=C_GOLD, width=2)

    # Bottom subtitle
    eb.text(40, H - 50, "Häusler & Baraghith (2023) · Biology & Philosophy 38:42",
            size=14, color=C_MUTED, font_family=5)

    return export(eb, 2)


# ── Slide 4: Three Flaws Comparison ─────────────────────────────────────────

def slide_04_three_flaws():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 560, 30, color=C_GOLD, width=3)

    # Column headers
    col1_x = 80
    col2_x = 680
    col_w = 520
    header_y = 80

    eb.rect(col1_x, header_y, col_w, 50, fill=C_BOX, stroke=C_BLUE)
    eb.text(col1_x + 15, header_y + 12, "Pandemic (Biological Virus)", size=18, color=C_BLUE, font_family=5)

    eb.rect(col2_x, header_y, col_w, 50, fill=C_BOX, stroke=C_RED)
    eb.text(col2_x + 15, header_y + 12, "Infodemic (Fake News)", size=18, color=C_RED, font_family=5)

    # Three rows
    rows = [
        ("Identification", "Clear pathogen:\nphysical viral particle", "Unclear entity:\nbelief? meme? post?", C_ORANGE),
        ("Intentionality", "Random mutation:\nno deliberate design", "Deliberate creation:\nactors intentionally spread", C_PURPLE),
        ("Control", "Health measures:\nquarantine, vaccines", "No clear countermeasures:\npolitical & epistemic barriers", C_RED),
    ]

    row_h = 140
    for i, (flaw, col1, col2, color) in enumerate(rows):
        y = header_y + 70 + i * (row_h + 15)

        # Flaw label
        eb.rect(col1_x, y, 120, row_h, fill=C_BOX, stroke=color)
        eb.text(col1_x + 8, y + row_h // 2 - 15, f"Flaw {i+1}\n{flaw}", size=15, color=color, font_family=5)

        # Col 1
        eb.rect(col1_x + 130, y, col_w - 130, row_h, fill=C_BOX, stroke=C_MUTED)
        eb.text(col1_x + 145, y + 15, col1, size=18, color=C_LIGHT, font_family=5)

        # Col 2
        eb.rect(col2_x, y, col_w, row_h, fill="#2A1520", stroke=C_RED)
        eb.text(col2_x + 15, y + 15, col2, size=18, color=C_LIGHT, font_family=5)

    # Simon & Camargo attribution
    eb.text(40, H - 40, "Simon & Camargo (2021)", size=14, color=C_MUTED, font_family=5)

    return export(eb, 4)


# ── Slide 6: CET Hierarchy ───────────────────────────────────────────────────

def slide_06_cet_hierarchy():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 640, 30, color=C_GOLD, width=3)

    # Root
    root_x, root_y, root_w, root_h = 490, 60, 300, 60
    eb.rect(root_x, root_y, root_w, root_h, fill=C_BOX, stroke=C_GOLD, name="root")
    eb.text(root_x + 15, root_y + 15, "Cultural Information", size=22, color=C_GOLD, font_family=5)

    # Level 2 — adjusted y positions since title removed
    micro_x, micro_y, micro_w, micro_h = 510, 190, 260, 60
    l2 = [
        (140, 190, 260, 60, "Social Learning\n& Imitation", C_BLUE),
        (micro_x, micro_y, micro_w, micro_h, "Microevolutionary\nForces", C_TEAL),
        (870, 190, 260, 60, "High-Fidelity\nDigital Copying", C_PURPLE),
    ]
    for x, y, w, h, lbl, color in l2:
        eb.rect(x, y, w, h, fill=C_BOX, stroke=color, name=lbl[:6])
        eb.text(x + 10, y + 8, lbl, size=18, color=C_WHITE, font_family=5)
        eb.arrow(root_x + root_w // 2, root_y + root_h,
                 x + w // 2, y, color=C_MUTED, width=1)

    # Level 3 — Forces: arrows come from "Microevolutionary Forces" node bottom
    forces = [
        (340, 330, 180, 55, "Transmission", C_TEAL),
        (540, 330, 180, 55, "Selection", C_TEAL),
        (740, 330, 180, 55, "Drift", C_TEAL),
        (940, 330, 180, 55, "Diffusion", C_TEAL),
    ]
    micro_bottom_x = micro_x + micro_w // 2  # center-bottom of Microevolutionary Forces
    micro_bottom_y = micro_y + micro_h
    for x, y, w, h, lbl, color in forces:
        eb.rect(x, y, w, h, fill=C_BOX, stroke=color)
        eb.text(x + 15, y + 15, lbl, size=18, color=C_WHITE, font_family=5)
        eb.arrow(micro_bottom_x, micro_bottom_y, x + w // 2, y, color=C_MUTED, width=1)

    # Ramsey quote
    eb.rect(60, 490, 1160, 80, fill="#0D1525", stroke=C_GOLD)
    eb.text(80, 502,
            '"Culture is information transmitted between individuals or groups [...].\nThe information must bring about the reproduction of a behavioral trait." — Ramsey (2012)',
            size=16, color=C_LIGHT, font_family=5)

    return export(eb, 6)


# ── Slide 7: Cognitive Bias Taxonomy ────────────────────────────────────────

def slide_07_biases():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 620, 30, color=C_GOLD, width=3)

    # Root
    eb.rect(490, 55, 300, 60, fill=C_BOX, stroke=C_GOLD, name="root")
    eb.text(500, 72, "Cultural Selection Biases", size=20, color=C_GOLD, font_family=5)

    # Two branches
    # Model-based biases
    eb.rect(80, 190, 280, 60, fill=C_BOX, stroke=C_BLUE, name="model")
    eb.text(95, 205, "Model-Based Biases", size=20, color=C_BLUE, font_family=5)
    eb.arrow(640, 115, 220, 190, color=C_MUTED, width=1)

    mb = [
        (50, 310, 180, 55, "Prestige\nBias", C_BLUE),
        (250, 310, 180, 55, "Similarity\nBias", C_BLUE),
        (450, 310, 180, 55, "Age Bias", C_BLUE),
    ]
    for x, y, w, h, lbl, color in mb:
        eb.rect(x, y, w, h, fill=C_BOX, stroke=color)
        eb.text(x + 15, y + 10, lbl, size=18, color=C_WHITE, font_family=5)
        eb.arrow(220, 250, x + w // 2, y, color=C_MUTED, width=1)

    # Content biases
    eb.rect(840, 190, 280, 60, fill=C_BOX, stroke=C_ORANGE, name="content")
    eb.text(855, 205, "Content Biases", size=20, color=C_ORANGE, font_family=5)
    eb.arrow(640, 115, 980, 190, color=C_MUTED, width=1)

    cb_items = [
        (650, 310, 150, 55, "Negativity\nBias", C_ORANGE),
        (820, 310, 150, 55, "Threat\nBias", C_RED),
        (990, 310, 150, 55, "MCI", C_PURPLE),
        (1150, 310, 140, 55, "HAD", C_TEAL),
    ]
    for x, y, w, h, lbl, color in cb_items:
        eb.rect(x, y, w, h, fill=C_BOX, stroke=color)
        eb.text(x + 10, y + 10, lbl, size=18, color=C_WHITE, font_family=5)
        eb.arrow(980, 250, x + w // 2, y, color=C_MUTED, width=1)

    # Effect box
    eb.rect(80, 430, 1120, 60, fill="#1A2A10", stroke=C_GREEN)
    eb.text(100, 445, "→ Each bias increases transmission probability of fake news variants", size=20, color=C_GREEN, font_family=5)

    # Legend
    eb.text(80, 520, "MCI = Minimally Counterintuitive   HAD = Hidden Agency Detection",
            size=16, color=C_MUTED, font_family=5)

    return export(eb, 7)


# ── Slide 9: Prestige Bias Comparison ───────────────────────────────────────

def slide_09_prestige():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 700, 30, color=C_GOLD, width=3)

    # Two columns
    col_w = 560
    col_h = 440
    col1_x, col2_x = 50, 670
    col_y = 90

    # Left: Regular users
    eb.rect(col1_x, col_y, col_w, col_h, fill=C_BOX, stroke=C_MUTED)
    eb.text(col1_x + 15, col_y + 12, "Regular Users", size=22, color=C_MUTED, font_family=5)
    eb.line(col1_x + 15, col_y + 45, col1_x + col_w - 15, col_y + 45, color=C_MUTED, width=1)

    regular_items = [
        "80% of fake news sources",
        "31% of interactions generated",
        "Low reach, local spreading",
        "Slow cascade, many hops",
    ]
    for i, item in enumerate(regular_items):
        eb.text(col1_x + 25, col_y + 65 + i * 80, f"• {item}", size=18, color=C_LIGHT, font_family=5)

    # Right: Prestige actors
    eb.rect(col2_x, col_y, col_w, col_h, fill="#1A1530", stroke=C_PURPLE)
    eb.text(col2_x + 15, col_y + 12, "Prestige Actors", size=22, color=C_PURPLE, font_family=5)
    eb.line(col2_x + 15, col_y + 45, col2_x + col_w - 15, col_y + 45, color=C_PURPLE, width=1)

    elite_items = [
        "20% of fake news sources",
        "69% of interactions generated",
        "Direct mass audience access",
        "Rapid top-down cascade",
    ]
    for i, item in enumerate(elite_items):
        eb.text(col2_x + 25, col_y + 65 + i * 80, f"• {item}", size=18, color=C_LIGHT, font_family=5)

    # Source
    eb.text(40, H - 40, "Brennen et al. (2020)", size=14, color=C_MUTED, font_family=5)

    # Trump/Bolsonaro example — enlarged box
    eb.rect(50, 570, 1180, 65, fill="#200A0A", stroke=C_RED)
    eb.text(70, 583, "Example: 100+ calls to Maryland poison control re disinfectant injection after Trump's suggestion (2020)",
            size=16, color=C_LIGHT, font_family=5)

    return export(eb, 9)


# ── Slide 11: Filter Bubble TRIM Cycle ──────────────────────────────────────

def slide_11_trim_cycle():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 900, 30, color=C_GOLD, width=3)

    cx, cy = 640, 390
    # Central node
    eb.ellipse(cx - 100, cy - 50, 200, 100, fill="#1A2840", stroke=C_GOLD, name="center")
    eb.text(cx - 80, cy - 20, "Filter\nBubble", size=20, color=C_GOLD, font_family=5)

    # 4 surrounding boxes forming a cycle
    nodes = [
        (cx - 80, cy - 250, 160, 70, "Algorithm\nPersonalization", C_BLUE, "algo"),
        (cx + 200, cy - 60, 200, 70, "Echo Chamber\nReinforcement", C_ORANGE, "echo"),
        (cx - 80, cy + 140, 160, 70, "Out-group\nBlocked", C_RED, "outgroup"),
        (cx - 380, cy - 60, 200, 70, "In-group\nHigh Retention", C_TEAL, "ingroup"),
    ]
    for x, y, w, h, lbl, color, name in nodes:
        eb.rect(x, y, w, h, fill=C_BOX, stroke=color, name=name)
        eb.text(x + 10, y + 10, lbl, size=18, color=C_WHITE, font_family=5)

    # Cycle arrows (clock-wise)
    # algo → echo
    eb.arrow(cx + 80, cy - 215, cx + 300, cy + 0 - 30, color=C_MUTED, width=2)
    # echo → outgroup
    eb.arrow(cx + 300, cy + 40, cx + 80, cy + 175, color=C_MUTED, width=2)
    # outgroup → ingroup
    eb.arrow(cx - 80, cy + 175, cx - 280, cy + 40, color=C_MUTED, width=2)
    # ingroup → algo
    eb.arrow(cx - 280, cy - 30, cx - 80, cy - 215, color=C_MUTED, width=2)

    # TRIM definition
    eb.rect(40, 600, 700, 65, fill="#0D1525", stroke=C_TEAL)
    eb.text(55, 612, "TRIM = Transmission Isolating Mechanism\n(CET concept: prevents cross-group information flow)",
            size=15, color=C_LIGHT, font_family=5)

    # Stat
    eb.rect(760, 600, 480, 65, fill="#0D1525", stroke=C_ORANGE)
    eb.text(775, 612, "78% of US adults aware of\n≥1 COVID fake news (Hamel et al. 2021)",
            size=15, color=C_LIGHT, font_family=5)

    return export(eb, 11)


# ── Slide 12: Diffusion/Retention Quadrant ───────────────────────────────────

def slide_12_quadrant():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 700, 30, color=C_GOLD, width=3)

    CX, CY = 640, 390

    # Axes
    eb.line(100, CY, W - 100, CY, color=C_MUTED, width=2)
    eb.line(CX, 90, CX, H - 60, color=C_MUTED, width=2)

    # Axis labels
    eb.text(105, CY + 10, "Low Diffusion", size=16, color=C_MUTED, font_family=5)
    eb.text(W - 250, CY + 10, "High Diffusion", size=16, color=C_MUTED, font_family=5)
    eb.text(CX + 10, 95, "High Retention", size=16, color=C_MUTED, font_family=5)
    eb.text(CX + 10, H - 80, "Low Retention", size=16, color=C_MUTED, font_family=5)

    # Axis arrow heads (labels)
    eb.text(CX - 130, 70, "↑ Retention Potential", size=16, color=C_LIGHT, font_family=5)
    eb.text(W - 320, CY - 30, "Diffusion Potential →", size=16, color=C_LIGHT, font_family=5)

    # Four quadrants
    bw, bh = 240, 130

    # Top-right: DANGER ZONE — high diffusion + high retention (fake news optimized)
    eb.rect(CX + 60, CY - 200, bw, bh, fill="#2A0A0A", stroke=C_RED)
    eb.text(CX + 75, CY - 190, "DANGER ZONE", size=16, color=C_RED, font_family=5, bold=True)
    eb.text(CX + 75, CY - 165, "Catchy + Sticky\n→ Filter bubble ideal\n(fake news optimized)", size=14, color=C_LIGHT, font_family=5)

    # Top-left: High retention only
    eb.rect(CX - 320, CY - 200, bw, bh, fill=C_BOX, stroke=C_PURPLE)
    eb.text(CX - 305, CY - 190, "Resistant but Niche", size=15, color=C_PURPLE, font_family=5)
    eb.text(CX - 305, CY - 165, "Stays in group\nnot widely spread\n(cult beliefs)", size=14, color=C_LIGHT, font_family=5)

    # Bottom-right: High diffusion, low retention
    eb.rect(CX + 60, CY + 50, bw, bh, fill=C_BOX, stroke=C_BLUE)
    eb.text(CX + 75, CY + 60, "Viral but Forgettable", size=14, color=C_BLUE, font_family=5)
    eb.text(CX + 75, CY + 85, "Spreads fast\nbut doesn't stick\n(memes, trends)", size=14, color=C_LIGHT, font_family=5)

    # Bottom-left: Neither
    eb.rect(CX - 320, CY + 50, bw, bh, fill=C_BOX, stroke=C_MUTED)
    eb.text(CX - 305, CY + 60, "Marginalized Info", size=14, color=C_MUTED, font_family=5)
    eb.text(CX - 305, CY + 85, "Fact-checks &\ncorrections live here\n(low reach + low stick)", size=14, color=C_LIGHT, font_family=5)

    # Quote — enlarged box
    eb.rect(40, 600, 1200, 75, fill="#0D1525", stroke=C_GOLD)
    eb.text(55, 610,
            '"A new variant may be very tempting [diffusion potential] [...] an individual addicted will have difficulties abandoning it [retention potential]" — Strimling et al. (2009)',
            size=15, color=C_LIGHT, font_family=5)

    return export(eb, 12)


# ── Slide 14: Self-Immunization Cycle ────────────────────────────────────────

def slide_14_immunization_cycle():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 770, 30, color=C_GOLD, width=3)

    # Circular arrangement of 4 nodes
    cx, cy = 640, 360
    r = 200

    import math
    node_data = [
        (0,   "Initial Fake\nNews Belief", C_RED),
        (90,  "Refutation\nAttempt", C_BLUE),
        (180, "Dissonance +\nRationalization", C_ORANGE),
        (270, "Belief\nReinforced", C_RED),
    ]

    node_ids = []
    for angle, label, color in node_data:
        rad = math.radians(angle - 90)
        nx = cx + r * math.cos(rad) - 100
        ny = cy + r * math.sin(rad) - 35
        nid = eb.rect(nx, ny, 200, 70, fill=C_BOX, stroke=color, name=f"n{angle}")
        node_ids.append((nx, ny, 200, 70, nid))
        eb.text(nx + 10, ny + 10, label, size=17, color=C_WHITE, font_family=5)

    # Cycle arrows between nodes
    angles = [0, 90, 180, 270]
    for i in range(4):
        a1 = angles[i]
        a2 = angles[(i + 1) % 4]
        rad1 = math.radians(a1 - 90)
        rad2 = math.radians(a2 - 90)
        x1 = cx + r * math.cos(rad1)
        y1 = cy + r * math.sin(rad1)
        x2 = cx + r * math.cos(rad2)
        y2 = cy + r * math.sin(rad2)
        eb.arrow(x1, y1, x2, y2, color=C_GOLD, width=2)

    # Center label
    eb.ellipse(cx - 90, cy - 40, 180, 80, fill="#1A0A0A", stroke=C_RED)
    eb.text(cx - 75, cy - 15, "Self-Sealing\nLoop", size=17, color=C_RED, font_family=5)

    # Side note
    eb.rect(40, 600, 700, 70, fill="#0D1525", stroke=C_ORANGE)
    eb.text(55, 613, '"Falsification = part of the conspiracy"\nPseudo-science mimics science style → hard to distinguish',
            size=15, color=C_LIGHT, font_family=5)

    eb.rect(760, 600, 480, 70, fill="#0D1525", stroke=C_MUTED)
    eb.text(775, 613, "Boudry & Braeckman (2012):\nCognitive immunization strategies",
            size=15, color=C_LIGHT, font_family=5)

    return export(eb, 14)


# ── Slide 15: Debunking vs Prebunking Comparison ─────────────────────────────

def slide_15_debunk_vs_prebunk():
    """Rendered with Pillow for pixel-perfect rounded corners."""
    from PIL import Image, ImageDraw, ImageFont
    import os

    SCALE = 2
    W, H = 1280 * SCALE, 720 * SCALE
    BG = "#121A2E"
    BOX = "#1E3050"
    RADIUS = 20  # dezent abgerundet

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Font helpers
    def font(size):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()

    def font_bold(size):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

    s = SCALE  # shorthand
    col_w, col_h = 520 * s, 520 * s
    col_y = 40 * s
    header_h = 50 * s

    # ── Debunking box ──
    bx = 40 * s
    draw.rounded_rectangle([(bx, col_y), (bx + col_w, col_y + col_h)],
                           radius=RADIUS, fill=BOX, outline=C_RED, width=3)
    draw.text((bx + 25*s, col_y + 10*s), "DEBUNKING ✗", fill=C_RED, font=font_bold(44))
    draw.text((bx + 260*s, col_y + 14*s), "After infection", fill="#E07070", font=font(32))
    # Divider
    line_y = col_y + header_h + 15*s
    draw.line([(bx + 25*s, line_y), (bx + col_w - 25*s, line_y)], fill=C_RED, width=2)

    debunk_items = [
        "• False claims spread —\n  correction always too late",
        "• Fact-checks spread 6× slower\n  than falsehoods (Vosoughi 2018)",
        "• Warnings backfire: trust in\n  TRUE news drops too",
    ]
    body_y = col_y + header_h + 30*s
    f_body = font(34)
    for i, item in enumerate(debunk_items):
        draw.text((bx + 25*s, body_y + i * 140*s), item, fill=C_LIGHT, font=f_body)

    # ── Prebunking box ──
    px = 720 * s
    draw.rounded_rectangle([(px, col_y), (px + col_w, col_y + col_h)],
                           radius=RADIUS, fill=BOX, outline=C_GREEN, width=3)
    draw.text((px + 25*s, col_y + 10*s), "PREBUNKING ✓", fill=C_GREEN, font=font_bold(44))
    draw.text((px + 260*s, col_y + 14*s), "Before infection", fill="#70C8A0", font=font(32))
    # Divider
    draw.line([(px + 25*s, line_y), (px + col_w - 25*s, line_y)], fill=C_GREEN, width=2)

    prebunk_items = [
        "• Pre-exposure builds resistance\n  before false beliefs form",
        "• Manipulation tactics exposed\n  in advance → inoculation",
        "• Cultural antibodies: critical\n  thinking generalizes broadly",
    ]
    for i, item in enumerate(prebunk_items):
        draw.text((px + 25*s, body_y + i * 140*s), item, fill=C_LIGHT, font=f_body)

    # ── VS circle ──
    vs_x, vs_y = 600*s, 265*s
    vs_r = 40*s
    draw.ellipse([(vs_x, vs_y), (vs_x + 2*vs_r, vs_y + 2*vs_r)],
                 fill=BOX, outline=C_GOLD, width=3)
    draw.text((vs_x + 14*s, vs_y + 14*s), "VS", fill=C_GOLD, font=font_bold(52))

    out_path = os.path.join("output", "images", "pandemic-infodemic_s15_diagram.png")
    img.save(out_path)
    print(f"  S15: {os.path.abspath(out_path)}")
    return os.path.abspath(out_path)


# ── Slide 16: Inoculation Flow ───────────────────────────────────────────────

def slide_16_inoculation_flow():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 680, 30, color=C_GOLD, width=3)

    # Flow: 4 steps horizontally
    steps = [
        ("Step 1", "Forewarning", "Alert about\nmanipulation tactics\nahead of exposure", C_BLUE),
        ("Step 2", "Prebunking", "Controlled exposure\nto weakened fake\nnews examples", C_ORANGE),
        ("Step 3", "Refutation\nPractice", "Participants\nactively counter\nfake arguments", C_PURPLE),
        ("Step 4", "Cultural\nAntibodies", "Critical thinking\ngeneralizes to\nnew fake news", C_GREEN),
    ]

    bw, bh = 240, 220
    gap = 40
    start_x = (W - 4 * bw - 3 * gap) // 2
    y = 110

    for i, (step, title, desc, color) in enumerate(steps):
        x = start_x + i * (bw + gap)
        eb.rect(x, y, bw, bh, fill=C_BOX, stroke=color)
        # Step badge
        eb.rect(x + 10, y + 10, 80, 28, fill=color, stroke=color)
        eb.text(x + 15, y + 13, step, size=15, color=C_BG, font_family=5, bold=True)
        eb.text(x + 15, y + 50, title, size=20, color=color, font_family=5)
        eb.line(x + 10, y + 80, x + bw - 20, y + 80, color=color, width=1)
        eb.text(x + 15, y + 90, desc, size=18, color=C_LIGHT, font_family=5)

        # Arrow between steps
        if i < 3:
            ax = x + bw
            ay = y + bh // 2
            eb.arrow(ax, ay, ax + gap, ay, color=C_GOLD, width=2)

    # Games row — split to two items to avoid overflow
    eb.rect(50, 380, 1180, 80, fill="#0A1A30", stroke=C_TEAL)
    eb.text(70, 393, "Real-world implementations:", size=18, color=C_TEAL, font_family=5, bold=True)
    eb.text(70, 420, '"Bad News" browser game  —  "Go Viral" (Facebook/DROG)  —  McGuire (1964) inoculation theory',
            size=18, color=C_LIGHT, font_family=5)

    # Medical analogy
    eb.rect(50, 500, 1180, 80, fill="#0D1525", stroke=C_GOLD)
    eb.text(70, 513, "Medical analogy: Vaccine exposes immune system to weakened pathogen →",
            size=18, color=C_LIGHT, font_family=5)
    eb.text(70, 541, "Psychological inoculation exposes mind to weakened manipulation → resistance generalizes",
            size=18, color=C_GOLD, font_family=5)

    return export(eb, 16)


# ── Slide 17: Pandemic ↔ Infodemic Comparison ────────────────────────────────

def slide_17_parallel():
    eb = ExcalidrawBuilder(dark=True, width=1280, height=720)
    W, H = 1280, 720

    # (No internal title — Slide title serves as header)
    eb.line(40, 30, 560, 30, color=C_GOLD, width=3)

    # Three columns: concept | pandemic | infodemic
    cols = [80, 360, 810]
    col_widths = [260, 430, 430]
    row_h = 88
    rows_y = [55, 155, 255, 355, 455, 555]

    headers = ["Concept", "Pandemic (Biology)", "Infodemic (CET)"]
    header_colors = [C_GOLD, C_BLUE, C_TEAL]
    for i, (hdr, color, cw) in enumerate(zip(headers, header_colors, col_widths)):
        eb.rect(cols[i], rows_y[0], cw, 65, fill=C_BOX, stroke=color)
        eb.text(cols[i] + 12, rows_y[0] + 18, hdr, size=20, color=color, font_family=5, bold=True)

    # Row data
    rows = [
        ("Spreading\nAgent", "Biological virus\n(pathogen)", "Cultural variant\n(fake news meme)"),
        ("Selection\nMechanism", "Fitness for replication\nin host cells", "Cognitive biases\n(negativity, prestige, MCI)"),
        ("Isolation\nBarrier", "Quarantine\nPhysical distance", "Filter bubbles\n= TRIMs"),
        ("Fitness\nConsequence", "Morbidity,\nmortality", "Anti-vax behavior,\nhealth non-compliance"),
        ("Solution", "Herd immunity\nVaccination", "Societal herd immunity\nPsychological inoculation"),
    ]
    row_colors = [C_ORANGE, C_PURPLE, C_TEAL, C_RED, C_GREEN]

    for r_idx, (concept, pandemic_val, infodemic_val) in enumerate(rows):
        y = rows_y[r_idx + 1]
        color = row_colors[r_idx]

        # Concept column
        eb.rect(cols[0], y, col_widths[0], row_h - 5, fill=C_BOX, stroke=color)
        eb.text(cols[0] + 12, y + 12, concept, size=16, color=color, font_family=5)

        # Pandemic column
        eb.rect(cols[1], y, col_widths[1], row_h - 5, fill=C_BOX, stroke=C_MUTED)
        eb.text(cols[1] + 12, y + 8, pandemic_val, size=17, color=C_LIGHT, font_family=5)

        # Infodemic column
        eb.rect(cols[2], y, col_widths[2], row_h - 5, fill=C_BOX, stroke=C_TEAL)
        eb.text(cols[2] + 12, y + 8, infodemic_val, size=17, color=C_LIGHT, font_family=5)

    # Footnote with source
    eb.text(80, 640, "CET provides the theoretical language to make the analogy precise — not just metaphorical",
            size=15, color=C_MUTED, font_family=5)
    eb.text(80, 668, "Source: Häusler & Baraghith (2023)", size=14, color=C_MUTED, font_family=5)

    return export(eb, 17)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Generating Excalidraw diagrams for pandemic-infodemic presentation...")
    results = {}

    fns = [
        (2, slide_02_roadmap),
        (4, slide_04_three_flaws),
        (6, slide_06_cet_hierarchy),
        (7, slide_07_biases),
        (9, slide_09_prestige),
        (11, slide_11_trim_cycle),
        (12, slide_12_quadrant),
        (14, slide_14_immunization_cycle),
        (15, slide_15_debunk_vs_prebunk),
        (16, slide_16_inoculation_flow),
        (17, slide_17_parallel),
    ]

    for num, fn in fns:
        results[num] = fn()

    ok_count = sum(1 for v in results.values() if v)
    fail_count = sum(1 for v in results.values() if not v)
    print(f"\nDone: {ok_count} OK, {fail_count} failed")
    print(json.dumps({"ok": fail_count == 0, "ok_count": ok_count, "fail_count": fail_count}))


if __name__ == "__main__":
    main()
