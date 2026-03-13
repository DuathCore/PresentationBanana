#!/usr/bin/env python3
"""
Generate all Excalidraw diagrams for v5 of the Baraghith presentation.
Each diagram is exported as a 1280x720 PNG.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_excalidraw import ExcalidrawBuilder

OUT = Path(__file__).parent.parent / "output" / "images"
OUT.mkdir(parents=True, exist_ok=True)
SLUG = "from-prompts-to-populations"

# ── Colors ────────────────────────────────────────────────────────────────
C_BG      = "#121A2E"
C_ACCENT  = "#F0AB00"
C_WHITE   = "#FFFFFF"
C_LIGHT   = "#C8D6E5"
C_MUTED   = "#7A8BA0"
C_BOX     = "#1E3050"
C_BOX2    = "#243B5E"
C_BLUE    = "#4A9EE0"
C_TEAL    = "#2EA89D"
C_GREEN   = "#3EB489"
C_PURPLE  = "#9B6DD0"
C_ORANGE  = "#E8853D"
C_RED     = "#E04B4B"

LEVEL = {3: C_ACCENT, 2: C_BLUE, 1: C_TEAL, 0: C_PURPLE}


def export(eb, slide_num):
    path = OUT / f"{SLUG}_s{slide_num:02d}_diagram_v5.png"
    eb.export_png(str(path), scale=2)
    print(f"  ✓ Slide {slide_num}: {path.name}")
    return str(path)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2: Practitioners Grid (2×3)
# ══════════════════════════════════════════════════════════════════════════
def diagram_02():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    practitioners = [
        ("Engineers", "architecture + weights", C_BLUE),
        ("RL Researchers", "behavioural policies", C_TEAL),
        ("Auditors", "instance traceability", C_GREEN),
        ("Roboticists", "embodiment + control", C_PURPLE),
        ("Governance", "purpose + context", C_ORANGE),
        ("Law", "accountable entity", C_RED),
    ]

    bw, bh = 370, 140
    gap = 30
    sx, sy = 30, 10

    for i, (who, what, color) in enumerate(practitioners):
        col, row = i % 3, i // 3
        x = sx + col * (bw + gap)
        y = sy + row * (bh + gap)
        eb.labeled_box(x, y, bw, bh, who, what,
                       fill=C_BOX, stroke=color, label_color=color,
                       sublabel_color=C_LIGHT, label_size=22, sublabel_size=16)

    eb.text(sx, 330, "Six criteria — six answers — frequent conflicts",
            size=18, color=C_ACCENT, align="left", width=1200)

    return export(eb, 2)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 3: Conflict Matrix
# ══════════════════════════════════════════════════════════════════════════
def diagram_03():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    conflicts = [
        ("Model", "Behaviour", "Same weights, different prompts → different behaviour", C_BLUE, C_TEAL),
        ("Model", "Instance ID", "One model → millions of sessions", C_BLUE, C_GREEN),
        ("Control-loop", "Model", "Same weights, different robot → different agent", C_PURPLE, C_BLUE),
        ("Instance ID", "Legal", "Millions of sessions → one accountable entity", C_GREEN, C_RED),
    ]

    rh = 110
    gap = 15
    sx = 30

    for i, (left, right, example, lc, rc) in enumerate(conflicts):
        y = 10 + i * (rh + gap)
        eb.rect(sx, y, 1220, rh, fill=C_BOX, stroke=C_BOX, stroke_width=1)
        eb.text(sx + 15, y + 15, left, size=20, color=lc)
        eb.text(sx + 200, y + 15, "≠", size=26, color=C_ACCENT)
        eb.text(sx + 240, y + 15, right, size=20, color=rc)
        eb.text(sx + 480, y + 15, example, size=15, color=C_LIGHT, width=700)

    eb.text(sx, 520, '"Each criterion targets a different level of organisation"',
            size=16, color=C_ACCENT, width=1200)

    return export(eb, 3)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5: Four Views Quadrant
# ══════════════════════════════════════════════════════════════════════════
def diagram_05():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    W, H = 1280, 720
    CX, CY = W / 2, H / 2 + 20

    # Axes
    eb.line(80, CY, W - 80, CY, color=C_MUTED, width=2)
    eb.line(CX, 30, CX, H - 30, color=C_MUTED, width=2)

    # Axis labels
    eb.text(80, CY + 12, "Weak individuation", size=14, color=C_MUTED)
    eb.text(W - 280, CY + 12, "Strong individuation", size=14, color=C_MUTED)
    eb.text(CX + 12, 30, "Agency in artifact", size=14, color=C_MUTED)
    eb.text(CX + 12, H - 50, "Agency in process", size=14, color=C_MUTED)

    bw, bh = 270, 110
    positions = [
        (150, 80, "Cabitza et al.", "Cybork: ensembles", C_TEAL),
        (W - bw - 150, 80, "Ferrario (2025)", "Artifact Realism", C_BLUE),
        (150, H - bh - 80, "Weinbaum & Veitas", "Process Ontology", C_PURPLE),
        (W - bw - 150, H - bh - 80, "Hawley (2019)", "Ontological Caution", C_ORANGE),
    ]

    for x, y, author, label, color in positions:
        eb.labeled_box(x, y, bw, bh, author, label,
                       fill=C_BOX, stroke=color, label_color=C_MUTED,
                       sublabel_color=color, label_size=16, sublabel_size=22)

    return export(eb, 5)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 6: Pivot — Quote + Flow
# ══════════════════════════════════════════════════════════════════════════
def diagram_06():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    # Quote box
    eb.rect(60, 30, 1160, 220, fill=C_BOX, stroke=C_ACCENT, stroke_width=2, roundness=3)
    eb.text(100, 55, '"These conflicts cannot be resolved by choosing\none \'true\' criterion — each targets a different\nlevel of organisation."',
            size=24, color=C_LIGHT, width=1080)
    eb.text(700, 195, "— Baraghith (2025)", size=16, color=C_ACCENT, width=400)

    # Flow: Pluralism → Meta-frame
    eb.labeled_box(200, 340, 280, 70, "Pluralism?", None,
                   fill=C_BOX, stroke=C_MUTED, label_color=C_MUTED, label_size=22)
    eb.arrow(490, 375, 600, 375, color=C_ACCENT, width=3)
    eb.labeled_box(610, 340, 350, 70, "Meta-frame needed", None,
                   fill=C_BOX, stroke=C_ACCENT, label_color=C_ACCENT, label_size=22)

    return export(eb, 6)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 8: CET vs Pluralism (2 columns)
# ══════════════════════════════════════════════════════════════════════════
def diagram_08():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    # Left: Pluralism
    eb.rect(30, 10, 580, 380, fill=C_BOX, stroke=C_MUTED, stroke_width=2, roundness=3)
    eb.text(50, 25, "Methodological Pluralism", size=22, color=C_MUTED)
    eb.line(50, 58, 250, 58, color=C_MUTED, width=2)

    plur = [("✓", "Tolerates multiple criteria", C_GREEN),
            ("✗", "Cannot explain WHY they exist", C_RED),
            ("✗", "No causal connections", C_RED)]
    for i, (mark, txt, c) in enumerate(plur):
        eb.text(50, 85 + i * 55, f"{mark}  {txt}", size=18, color=c, width=520)

    # Right: CET
    eb.rect(670, 10, 580, 380, fill=C_BOX, stroke=C_ACCENT, stroke_width=2, roundness=3)
    eb.text(690, 25, "Cultural Evolutionary Theory", size=22, color=C_ACCENT)
    eb.line(690, 58, 940, 58, color=C_ACCENT, width=2)

    cet = ["Explains criteria via levels", "Predicts which cluster", "One coupled system"]
    for i, txt in enumerate(cet):
        eb.text(690, 85 + i * 55, f"✓  {txt}", size=18, color=C_GREEN, width=520)

    # Arrow between
    eb.arrow(620, 190, 660, 190, color=C_ACCENT, width=3)

    return export(eb, 8)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 9: V/I/S Pillars (3 columns)
# ══════════════════════════════════════════════════════════════════════════
def diagram_09():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    pillars = [
        ("Variation", ["New architectures", "Fine-tuning"], C_BLUE),
        ("Inheritance", ["Model cloning", "API deployment"], C_TEAL),
        ("Selection", ["Benchmarks + RLHF", "Market adoption"], C_ACCENT),
    ]

    bw = 370
    gap = 35
    sx = 50

    for i, (title, items, color) in enumerate(pillars):
        x = sx + i * (bw + gap)
        eb.rect(x, 10, bw, 360, fill=C_BOX, stroke=color, stroke_width=2, roundness=3)
        eb.line(x + 15, 50, x + bw - 15, 50, color=color, width=2)
        eb.text(x + 15, 15, title, size=24, color=color, width=bw - 30)
        for j, item in enumerate(items):
            eb.text(x + 30, 75 + j * 55, item, size=18, color=C_LIGHT, width=bw - 60)

    eb.text(50, 400, "The three conditions for cultural evolution are met",
            size=16, color=C_ACCENT, width=1200)

    return export(eb, 9)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 11: Four-Level Hierarchy (core diagram)
# ══════════════════════════════════════════════════════════════════════════
def diagram_11():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    levels = [
        (3, "Model Lineages", "≈ Genetic lineages", "months–years"),
        (2, "Configured Systems", "≈ Organisms", "days–weeks"),
        (1, "Episodes & Instances", "≈ Interactions", "real-time"),
        (0, "Circulating Outputs", "≈ Cultural memes", "sec–years"),
    ]

    bw, bh = 700, 80
    gap = 30
    sx = 250

    for i, (lvl, name, analogy, timescale) in enumerate(levels):
        y = 10 + i * (bh + gap)
        color = LEVEL[lvl]
        eb.rect(sx, y, bw, bh, fill=C_BOX, stroke=color, stroke_width=2, roundness=3)
        # Color bar left
        eb.rect(sx, y, 6, bh, fill=color, stroke=color, stroke_width=0)
        eb.text(sx + 15, y + 10, f"Level {lvl}", size=18, color=color, width=100)
        eb.text(sx + 130, y + 10, name, size=20, color=C_WHITE, width=300)
        eb.text(sx + 460, y + 10, analogy, size=15, color=C_MUTED, width=220)
        eb.text(sx + 130, y + 45, timescale, size=13, color=C_MUTED, width=200)

        # Arrows between levels
        if i < 3:
            eb.arrow(sx + bw / 2, y + bh + 2, sx + bw / 2, y + bh + gap - 2,
                     color=LEVEL[levels[i + 1][0]], width=2)

    # Side labels
    eb.text(50, 50, "HIGHER\nabstraction", size=14, color=C_MUTED, width=160)
    eb.text(50, 350, "LOWER\nabstraction", size=14, color=C_MUTED, width=160)
    eb.line(120, 95, 120, 340, color=C_MUTED, width=1)
    eb.arrow(120, 340, 120, 380, color=C_MUTED, width=2)

    return export(eb, 11)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 12: V/T/S Table
# ══════════════════════════════════════════════════════════════════════════
def diagram_12():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    headers = ["Level", "Variation", "Transmission", "Selection"]
    hw = [220, 320, 320, 320]
    hx = [30]
    for i in range(1, 4):
        hx.append(hx[-1] + hw[i - 1] + 10)

    rh_header = 40
    rh = 60
    gap = 8

    # Header
    for i, (h, w, x) in enumerate(zip(headers, hw, hx)):
        eb.rect(x, 10, w, rh_header, fill=C_ACCENT, stroke=C_ACCENT, stroke_width=0)
        eb.text(x + 10, 15, h, size=16, color=C_BG)

    rows = [
        (3, "L3: Models", "architectures", "cloning, distillation", "benchmarks"),
        (2, "L2: Systems", "tools, prompts", "templating, configs", "cost, regulation"),
        (1, "L1: Episodes", "context, seeds", "training data", "user feedback"),
        (0, "L0: Outputs", "sampling, edits", "sharing, scraping", "attention, ranking"),
    ]

    sy = 10 + rh_header + gap
    for ri, (lvl, label, v, t, s) in enumerate(rows):
        y = sy + ri * (rh + gap)
        color = LEVEL[lvl]
        for ci, (w, x) in enumerate(zip(hw, hx)):
            eb.rect(x, y, w, rh, fill=C_BOX, stroke=C_BOX, stroke_width=1)
        eb.rect(hx[0], y, 5, rh, fill=color, stroke=color, stroke_width=0)
        eb.text(hx[0] + 12, y + 15, label, size=16, color=color, width=hw[0] - 20)
        eb.text(hx[1] + 12, y + 15, v, size=14, color=C_LIGHT, width=hw[1] - 20)
        eb.text(hx[2] + 12, y + 15, t, size=14, color=C_LIGHT, width=hw[2] - 20)
        eb.text(hx[3] + 12, y + 15, s, size=14, color=C_LIGHT, width=hw[3] - 20)

    return export(eb, 12)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 13: Cross-Level Causation
# ══════════════════════════════════════════════════════════════════════════
def diagram_13():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    bw, bh = 300, 65
    cx = 490
    sy = 30
    gap = 55
    names = [(3, "L3: Models"), (2, "L2: Systems"), (1, "L1: Episodes"), (0, "L0: Outputs")]

    for i, (lvl, name) in enumerate(names):
        y = sy + i * (bh + gap)
        color = LEVEL[lvl]
        eb.rect(cx, y, bw, bh, fill=C_BOX, stroke=color, stroke_width=2, roundness=3, name=f"L{lvl}")
        eb.text(cx + 15, y + 15, name, size=20, color=color, width=bw - 30)

    # Downward (left side) — red
    dx = cx - 60
    for i in range(3):
        y1 = sy + i * (bh + gap) + bh
        y2 = sy + (i + 1) * (bh + gap)
        eb.arrow(dx, y1 + 5, dx, y2 - 5, color=C_RED, width=3)
    eb.text(dx - 130, 200, "CONSTRAINS ↓", size=16, color=C_RED, width=150)
    eb.line(dx, sy + bh, dx, sy + 3 * (bh + gap), color=C_RED, width=1, style="dashed")

    # Upward (right side) — green
    ux = cx + bw + 60
    for i in range(3):
        y1 = sy + (i + 1) * (bh + gap)
        y2 = sy + i * (bh + gap) + bh
        eb.arrow(ux, y1 - 5, ux, y2 + 5, color=C_GREEN, width=3)
    eb.text(ux + 20, 200, "↑ AGGREGATES", size=16, color=C_GREEN, width=160)
    eb.line(ux, sy + bh, ux, sy + 3 * (bh + gap), color=C_GREEN, width=1, style="dashed")

    # Bypass L0→L3 (gold, left far side)
    bx = 80
    top_y = sy + bh / 2
    bot_y = sy + 3 * (bh + gap) + bh / 2
    eb.line(bx, top_y, bx, bot_y, color=C_ACCENT, width=3)
    eb.line(bx, top_y, cx, top_y, color=C_ACCENT, width=2, style="dashed")
    eb.line(bx, bot_y, cx, bot_y, color=C_ACCENT, width=2, style="dashed")
    eb.arrow(bx, bot_y - 10, bx, top_y + 10, color=C_ACCENT, width=3)
    eb.text(30, 260, "L0 → L3\nDirect\nfeedback", size=14, color=C_ACCENT, width=120)

    return export(eb, 13)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 14: Criteria → Levels Mapping
# ══════════════════════════════════════════════════════════════════════════
def diagram_14():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    mappings = [
        (3, "Level 3: Models", ["Model-instance", "Behavioural"], "Heritable information"),
        (2, "Level 2: Systems", ["Purpose", "Control-loop"], "Functional integration"),
        (1, "Level 1: Episodes", ["Instance ID"], "Selection events"),
        ("N", "Normative Overlay", ["Legal personhood"], "Applied to any level"),
    ]

    rh = 75
    gap = 15
    sy = 10

    for i, (lvl, label, criteria, role) in enumerate(mappings):
        y = sy + i * (rh + gap)
        color = LEVEL.get(lvl, C_MUTED)

        # Level box
        eb.rect(30, y, 240, rh, fill=C_BOX, stroke=color, stroke_width=2, roundness=3)
        eb.text(45, y + 20, label, size=17, color=color, width=210)

        # Arrow
        eb.arrow(280, y + rh / 2, 330, y + rh / 2, color=color, width=2)

        # Criteria boxes
        for j, crit in enumerate(criteria):
            cx = 340 + j * 250
            eb.rect(cx, y + 8, 230, rh - 16, fill=C_BOX2, stroke=color, stroke_width=2, roundness=3)
            eb.text(cx + 12, y + 22, crit, size=16, color=C_WHITE, width=206)

        # Role
        eb.text(860, y + 22, role, size=14, color=C_MUTED, width=300)

    eb.text(30, 380, "Conflicts resolved: criteria target different levels, not the same object",
            size=16, color=C_ACCENT, width=1200)

    return export(eb, 14)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 15: RLHF Diamond Cycle
# ══════════════════════════════════════════════════════════════════════════
def diagram_15():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    nw, nh = 260, 70
    # Diamond: L3 top, L2 right, L1 bottom, L0 left
    nodes = [
        (510, 30, 3, "L3: Models"),
        (870, 220, 2, "L2: Systems"),
        (510, 410, 1, "L1: Episodes"),
        (150, 220, 0, "L0: Outputs"),
    ]

    for x, y, lvl, label in nodes:
        color = LEVEL[lvl]
        eb.rect(x, y, nw, nh, fill=C_BOX, stroke=color, stroke_width=2, roundness=3, name=f"rlhf_L{lvl}")
        eb.text(x + 15, y + 18, label, size=20, color=color, width=nw - 30)

    # Cycle arrows (clockwise): L3→L2→L1→L0→L3
    # L3 right edge → L2 top
    eb.arrow(770, 65, 870, 220, color=C_ACCENT, width=2)
    # L2 bottom → L1 right edge
    eb.arrow(1000, 290, 770, 410, color=C_ACCENT, width=2)
    # L1 left edge → L0 bottom
    eb.arrow(510, 445, 410, 290, color=C_ACCENT, width=2)
    # L0 top → L3 left edge
    eb.arrow(280, 220, 510, 65, color=C_ACCENT, width=2)

    # Center label
    eb.text(440, 240, "RLHF\nCycle", size=22, color=C_ACCENT, width=120)

    eb.text(330, 520, "No single level owns the process",
            size=18, color=C_ACCENT, width=600)

    return export(eb, 15)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 16: Governance (4 columns)
# ══════════════════════════════════════════════════════════════════════════
def diagram_16():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    interventions = [
        (3, "Training", "data + weights", "broadest", C_ACCENT),
        (2, "Systems", "oversight + audit", "targeted", C_BLUE),
        (1, "Episodes", "consent + feedback", "fine-grained", C_TEAL),
        (0, "Outputs", "watermarks + labels", "environmental", C_PURPLE),
    ]

    bw = 260
    bh = 320
    gap = 40
    sx = 50

    for i, (lvl, title, what, scope, color) in enumerate(interventions):
        x = sx + i * (bw + gap)
        eb.rect(x, 10, bw, bh, fill=C_BOX, stroke=color, stroke_width=2, roundness=3)
        eb.line(x + 10, 50, x + bw - 10, 50, color=color, width=2)
        eb.text(x + 12, 18, f"Level {lvl}", size=14, color=C_MUTED, width=bw - 24)
        eb.text(x + 12, 60, title, size=22, color=color, width=bw - 24)
        eb.text(x + 12, 120, what, size=16, color=C_LIGHT, width=bw - 24)
        eb.text(x + 12, 265, scope, size=16, color=color, width=bw - 24)

        if i < 3:
            eb.arrow(x + bw + 5, 170, x + bw + gap - 5, 170, color=C_ACCENT, width=2)

    eb.text(50, 360, "Each intervention cascades differently through the coupled system",
            size=16, color=C_ACCENT, width=1200)

    return export(eb, 16)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 17: Descriptive vs Normative (2 columns)
# ══════════════════════════════════════════════════════════════════════════
def diagram_17():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    # Left: Descriptive
    eb.rect(30, 10, 560, 370, fill=C_BOX, stroke=C_TEAL, stroke_width=2, roundness=3)
    eb.text(50, 25, "Descriptive (CET)", size=22, color=C_TEAL)
    eb.line(50, 58, 270, 58, color=C_TEAL, width=2)

    desc = ["How do AI systems vary?", "How are traits inherited?", "What gets selected, and why?"]
    for i, item in enumerate(desc):
        eb.text(60, 85 + i * 55, item, size=20, color=C_LIGHT, width=500)

    # Right: Normative
    eb.rect(690, 10, 560, 370, fill=C_BOX, stroke=C_PURPLE, stroke_width=2, roundness=3)
    eb.text(710, 25, "Normative (Ethics/Law)", size=22, color=C_PURPLE)
    eb.line(710, 58, 960, 58, color=C_PURPLE, width=2)

    norm = ["Which AI deserves moral status?", "Who bears responsibility?", "What should be regulated?"]
    for i, item in enumerate(norm):
        eb.text(720, 85 + i * 55, item, size=20, color=C_LIGHT, width=500)

    # Bridge arrow
    eb.arrow(590, 180, 690, 180, color=C_ACCENT, width=2)
    eb.text(600, 148, "informs →", size=14, color=C_ACCENT, width=100)

    eb.text(300, 410, "CET informs but does not determine",
            size=18, color=C_ACCENT, width=600)

    return export(eb, 17)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 18: Future Work (3 items)
# ══════════════════════════════════════════════════════════════════════════
def diagram_18():
    eb = ExcalidrawBuilder(dark=True)
    eb.set_background(C_BG)

    items = [
        "Explicit reproduction predicates per level",
        "Level-specific fitness notions",
        "Pressure-testing on concrete governance cases",
    ]

    for i, item in enumerate(items):
        y = 30 + i * 120
        eb.rect(100, y, 1060, 85, fill=C_BOX, stroke=C_ACCENT, stroke_width=2, roundness=3)
        eb.text(125, y + 18, str(i + 1), size=32, color=C_ACCENT, width=40)
        eb.text(185, y + 25, item, size=22, color=C_LIGHT, width=950)

    return export(eb, 18)


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    print("Generating Excalidraw diagrams for v5...")
    results = {}
    for fn in [diagram_02, diagram_03, diagram_05, diagram_06, diagram_08,
               diagram_09, diagram_11, diagram_12, diagram_13, diagram_14,
               diagram_15, diagram_16, diagram_17, diagram_18]:
        name = fn.__name__
        num = int(name.split("_")[1])
        results[num] = fn()

    print(f"\nDone! {len(results)} diagrams generated.")
    print(json.dumps({"ok": True, "diagrams": len(results), "paths": results}, indent=2))


if __name__ == "__main__":
    main()
