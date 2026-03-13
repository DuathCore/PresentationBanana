#!/usr/bin/env python3
"""
PresentationBanana — Excalidraw Diagram Generator
===================================================
Generates .excalidraw JSON files programmatically and exports to PNG.
Requires: npm install -g @moona3k/excalidraw-export

Usage:
    # From other scripts:
    from generate_excalidraw import ExcalidrawBuilder
    eb = ExcalidrawBuilder(dark=True)
    eb.rect(100, 100, 300, 80, fill="#1E3050", stroke="#F0AB00")
    eb.text(120, 115, "Hello World", size=24, color="#FFFFFF")
    eb.arrow_between("id1", "id2")
    eb.save("output.excalidraw")
    eb.export_png("output.png", scale=2)
"""

import json
import subprocess
import sys
import uuid
from pathlib import Path


def _id():
    return uuid.uuid4().hex[:20]


class ExcalidrawBuilder:
    """Programmatic builder for Excalidraw JSON files."""

    def __init__(self, dark=True, width=1280, height=720):
        self.elements = []
        self.files = {}
        self.dark = dark
        self.width = width
        self.height = height
        self.bg_color = "#121A2E" if dark else "#ffffff"
        self._id_map = {}  # name -> element id

    # ── Primitive elements ────────────────────────────────────────────────

    def rect(self, x, y, w, h, fill="#1E3050", stroke="#F0AB00",
             stroke_width=2, stroke_style="solid", fill_style="solid",
             roundness=3, opacity=100, name=None):
        """Add a rectangle. Returns element id."""
        eid = _id()
        el = {
            "id": eid, "type": "rectangle",
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": fill,
            "fillStyle": fill_style,
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "roughness": 0,
            "opacity": opacity,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": roundness} if roundness else None,
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
        }
        self.elements.append(el)
        if name:
            self._id_map[name] = eid
        return eid

    def diamond(self, x, y, w, h, fill="#1E3050", stroke="#F0AB00",
                stroke_width=2, opacity=100, name=None):
        """Add a diamond shape. Returns element id."""
        eid = _id()
        el = {
            "id": eid, "type": "diamond",
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": fill,
            "fillStyle": "solid",
            "strokeWidth": stroke_width,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": opacity,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 2},
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
        }
        self.elements.append(el)
        if name:
            self._id_map[name] = eid
        return eid

    def ellipse(self, x, y, w, h, fill="#1E3050", stroke="#F0AB00",
                stroke_width=2, opacity=100, name=None):
        """Add an ellipse. Returns element id."""
        eid = _id()
        el = {
            "id": eid, "type": "ellipse",
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": fill,
            "fillStyle": "solid",
            "strokeWidth": stroke_width,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": opacity,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 2},
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
        }
        self.elements.append(el)
        if name:
            self._id_map[name] = eid
        return eid

    def text(self, x, y, text, size=20, color="#FFFFFF", align="left",
             bold=False, font_family=5, width=None, name=None):
        """Add text. font_family: 1=Virgil(hand), 5=Helvetica, 7=Cascadia(mono)."""
        eid = _id()
        # Estimate width if not given
        if width is None:
            max_line = max(text.split("\n"), key=len)
            width = len(max_line) * size * 0.6
        lines = text.count("\n") + 1
        height = lines * size * 1.25
        el = {
            "id": eid, "type": "text",
            "x": x, "y": y,
            "width": width, "height": height,
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
            "text": text,
            "fontSize": size,
            "fontFamily": font_family,
            "textAlign": align,
            "verticalAlign": "top",
            "containerId": None,
            "originalText": text,
            "autoResize": True,
            "lineHeight": 1.25,
        }
        self.elements.append(el)
        if name:
            self._id_map[name] = eid
        return eid

    def line(self, x1, y1, x2, y2, color="#F0AB00", width=2, style="solid"):
        """Add a line from (x1,y1) to (x2,y2)."""
        eid = _id()
        el = {
            "id": eid, "type": "line",
            "x": x1, "y": y1,
            "width": abs(x2 - x1), "height": abs(y2 - y1),
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": width,
            "strokeStyle": style,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 2},
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": None,
        }
        self.elements.append(el)
        return eid

    def arrow(self, x1, y1, x2, y2, color="#F0AB00", width=2,
              style="solid", start_id=None, end_id=None,
              start_arrowhead=None, end_arrowhead="arrow"):
        """Add an arrow. Optionally bind to elements by id/name."""
        eid = _id()
        # Resolve names to ids
        if start_id and start_id in self._id_map:
            start_id = self._id_map[start_id]
        if end_id and end_id in self._id_map:
            end_id = self._id_map[end_id]

        start_binding = None
        end_binding = None
        if start_id:
            start_binding = {
                "elementId": start_id,
                "focus": 0, "gap": 5, "fixedPoint": None,
            }
            # Add boundElements ref to source
            for el in self.elements:
                if el["id"] == start_id:
                    el["boundElements"].append({"id": eid, "type": "arrow"})
        if end_id:
            end_binding = {
                "elementId": end_id,
                "focus": 0, "gap": 5, "fixedPoint": None,
            }
            for el in self.elements:
                if el["id"] == end_id:
                    el["boundElements"].append({"id": eid, "type": "arrow"})

        el = {
            "id": eid, "type": "arrow",
            "x": x1, "y": y1,
            "width": abs(x2 - x1), "height": abs(y2 - y1),
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": width,
            "strokeStyle": style,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": {"type": 2},
            "seed": hash(eid) % 2**31,
            "version": 1, "versionNonce": 0,
            "isDeleted": False,
            "boundElements": [],
            "updated": 0, "link": None, "locked": False,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None,
            "startBinding": start_binding,
            "endBinding": end_binding,
            "startArrowhead": start_arrowhead,
            "endArrowhead": end_arrowhead,
        }
        self.elements.append(el)
        return eid

    # ── High-level helpers ────────────────────────────────────────────────

    def labeled_box(self, x, y, w, h, label, sublabel=None,
                    fill="#1E3050", stroke="#F0AB00", label_color="#FFFFFF",
                    sublabel_color="#C8D6E5", label_size=20, sublabel_size=14,
                    name=None):
        """Rectangle with centered label and optional sublabel."""
        rid = self.rect(x, y, w, h, fill=fill, stroke=stroke, name=name)
        # Center label
        self.text(x + 10, y + (h / 2 - label_size * 0.7) if not sublabel else y + h * 0.2,
                  label, size=label_size, color=label_color, align="left")
        if sublabel:
            self.text(x + 10, y + h * 0.55, sublabel,
                      size=sublabel_size, color=sublabel_color, align="left")
        return rid

    def labeled_diamond(self, x, y, w, h, label, fill="#1E3050",
                        stroke="#F0AB00", label_color="#FFFFFF",
                        label_size=16, name=None):
        """Diamond with centered label."""
        did = self.diamond(x, y, w, h, fill=fill, stroke=stroke, name=name)
        self.text(x + w * 0.2, y + h * 0.35, label,
                  size=label_size, color=label_color, align="center",
                  width=w * 0.6)
        return did

    # ── Background ────────────────────────────────────────────────────────

    def set_background(self, color):
        self.bg_color = color

    # ── Export ────────────────────────────────────────────────────────────

    def to_dict(self):
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "PresentationBanana",
            "elements": self.elements,
            "appState": {
                "gridSize": None,
                "gridStep": 5,
                "gridModeEnabled": False,
                "viewBackgroundColor": self.bg_color,
            },
            "files": self.files,
        }

    def save(self, path):
        """Save as .excalidraw JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f)
        return str(path)

    def export_png(self, png_path, scale=2):
        """Export to PNG via excalidraw-export CLI. Returns path or raises."""
        # First save temp .excalidraw
        tmp = Path(png_path).with_suffix(".excalidraw")
        self.save(tmp)

        png_path = Path(png_path)
        png_path.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ["excalidraw-export", str(tmp), "-o", str(png_path), "--scale", str(scale)],
            capture_output=True, text=True, timeout=30,
        )
        # Clean up temp file
        tmp.unlink(missing_ok=True)

        if result.returncode != 0:
            raise RuntimeError(f"excalidraw-export failed: {result.stderr}")
        return str(png_path)


# ── CLI test ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Demo: generate the Slide 5 quadrant diagram
    eb = ExcalidrawBuilder(dark=True)

    W, H = 1280, 720
    CX, CY = W / 2, H / 2

    # Colors matching presentation theme
    C_BG = "#121A2E"
    C_ACCENT = "#F0AB00"
    C_MUTED = "#7A8BA0"
    C_BOX = "#1E3050"
    C_BLUE = "#4A9EE0"
    C_TEAL = "#2EA89D"
    C_PURPLE = "#9B6DD0"
    C_ORANGE = "#E8853D"
    C_WHITE = "#FFFFFF"
    C_LIGHT = "#C8D6E5"

    eb.set_background(C_BG)

    # Title
    eb.text(40, 20, "Four positions span individuation and agency",
            size=28, color=C_WHITE, font_family=5)
    eb.line(40, 58, 500, 58, color=C_ACCENT, width=3)

    # Axes
    eb.line(100, CY, W - 100, CY, color=C_MUTED, width=2)   # horizontal
    eb.line(CX, 90, CX, H - 40, color=C_MUTED, width=2)     # vertical

    # Axis labels
    eb.text(100, CY + 10, "Weak individuation", size=14, color=C_MUTED)
    eb.text(W - 300, CY + 10, "Strong individuation", size=14, color=C_MUTED)
    eb.text(CX + 10, 90, "Agency in artifact", size=14, color=C_MUTED)
    eb.text(CX + 10, H - 55, "Agency in process", size=14, color=C_MUTED)

    # Quadrant boxes
    bw, bh = 260, 100

    # Top-left: Cabitza (weak + artifact)
    eb.labeled_box(150, 150, bw, bh, "Cabitza et al.", "Cybork: ensembles",
                   fill=C_BOX, stroke=C_TEAL, label_color=C_TEAL,
                   sublabel_color=C_LIGHT, name="cabitza")

    # Top-right: Ferrario (strong + artifact)
    eb.labeled_box(W - bw - 150, 150, bw, bh, "Ferrario (2025)", "Artifact Realism",
                   fill=C_BOX, stroke=C_BLUE, label_color=C_BLUE,
                   sublabel_color=C_LIGHT, name="ferrario")

    # Bottom-left: Weinbaum (weak + process)
    eb.labeled_box(150, H - bh - 90, bw, bh, "Weinbaum & Veitas", "Process Ontology",
                   fill=C_BOX, stroke=C_PURPLE, label_color=C_PURPLE,
                   sublabel_color=C_LIGHT, name="weinbaum")

    # Bottom-right: Hawley (strong + process)
    eb.labeled_box(W - bw - 150, H - bh - 90, bw, bh, "Hawley (2019)", "Ontological Caution",
                   fill=C_BOX, stroke=C_ORANGE, label_color=C_ORANGE,
                   sublabel_color=C_LIGHT, name="hawley")

    # Export
    out_dir = Path(__file__).parent.parent / "output" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / "from-prompts-to-populations_s05_excalidraw.png"

    try:
        result = eb.export_png(str(png_path), scale=2)
        print(json.dumps({"ok": True, "path": result}))
    except Exception as e:
        # Fallback: save .excalidraw only
        exc_path = out_dir / "from-prompts-to-populations_s05.excalidraw"
        eb.save(exc_path)
        print(json.dumps({"ok": False, "error": str(e),
                          "excalidraw": str(exc_path)}))
