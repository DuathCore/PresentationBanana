---
name: scientific-presentation
description: Create academic/scientific PowerPoint presentations from papers, PDFs, or topics. Uses Excalidraw diagrams, Imagen for atmosphere images, Bull & Bear critique loops, and strict academic design rules. Invoke when user wants a university-quality scientific presentation.
argument-hint: [path-to-pdf-or-topic]
---

# Scientific Presentation Skill

Du erstellst akademische Präsentationen in Universitäts-Qualität.
Input: PDF-Paper, Topic-Beschreibung oder bestehendes PPTX.

**Projektverzeichnis:** /home/marek/PresentationBanana/
**Regelwerk:** Lies IMMER zuerst die Design-Regeln in `/root/.claude/projects/-home-marek/memory/reference_academic_presentation_rules.md`

---

## Verfügbare Tools

### 1. Excalidraw Diagram Generator (`scripts/generate_excalidraw.py`)
Erzeugt programmatische Diagramme als PNG via Excalidraw JSON → Export.
Für: Hierarchien, Flowcharts, Quadranten, Vergleiche, Mappings, Zyklen, Tabellen.

```python
from generate_excalidraw import ExcalidrawBuilder
eb = ExcalidrawBuilder(dark=True)
eb.rect(x, y, w, h, fill, stroke)          # Rechteck
eb.diamond(x, y, w, h, fill, stroke)       # Raute (Entscheidungen)
eb.ellipse(x, y, w, h, fill, stroke)       # Ellipse
eb.text(x, y, "Text", size=20, color="#FFF") # Text
eb.line(x1, y1, x2, y2, color)             # Linie
eb.arrow(x1, y1, x2, y2, color)            # Pfeil
eb.labeled_box(x, y, w, h, "Label", "Sublabel", fill, stroke, name="id")
eb.labeled_diamond(x, y, w, h, "Label", fill, stroke, name="id")
eb.export_png("output.png", scale=2)       # → PNG export
```

**Canvas:** 1280×720 (16:9) Standard. Dunkler Hintergrund #121A2E.
**Vorteile:** Exakter Text, Farb-Kontrolle, skalierbar, reproduzierbar.
**Export:** `excalidraw-export` CLI (npm, bereits installiert).

### 2. Imagen Image Generator (`scripts/generate_image.py`)
Erzeugt atmosphärische Bilder via Google Imagen 4. NUR für:
- Title Slide (stimmungsvoll)
- Section Divider (thematisch-abstrakt)
- Closing Slide (einprägsam)

```bash
python3 scripts/generate_image.py \
  --slide N --prompt "..." --version 1 --slide-type [title|section|closing]
```

**NIEMALS für Content-Slides!** Imagen kann keinen zuverlässigen Text.

### 3. Excalidraw MCP Server (localhost:3000)
Live-Canvas für iteratives Diagramm-Verfeinern. 26 MCP-Tools verfügbar.
Canvas muss laufen: `cd .mcp_excalidraw && PORT=3000 node dist/server.js &`

Wichtige MCP-Tools:
- `mcp__excalidraw__create_element` — Element erstellen (rectangle, text, arrow, diamond, ellipse)
- `mcp__excalidraw__batch_create_elements` — Mehrere Elemente auf einmal
- `mcp__excalidraw__update_element` — Element ändern
- `mcp__excalidraw__export_to_image` — Canvas als PNG/SVG exportieren
- `mcp__excalidraw__create_from_mermaid` — Mermaid-Syntax → Diagramm
- `mcp__excalidraw__get_canvas_screenshot` — Vorschau holen

**Wann MCP statt Generator:** Wenn iteratives Verfeinern nötig ist (Bull & Bear Fixes).
**Wann Generator:** Wenn das Diagramm in einem Durchlauf stehen soll.

### 4. Matplotlib Chart Generator (`scripts/generate_chart.py`)
Für Datenvisualisierung: Graphen, Balken, Scatter, Pie Charts.
Excalidraw kann keine Daten-Plots — Matplotlib füllt diese Lücke.

```python
from generate_chart import ChartBuilder
cb = ChartBuilder()
cb.bar_chart(["A", "B", "C"], [10, 20, 15], "Title", "Y-Label")
cb.line_chart(x, [y1, y2], "Title", "X", "Y", labels=["Ser1", "Ser2"])
cb.scatter_plot(x, y, "Title", "X", "Y")
cb.pie_chart(["A", "B"], [60, 40], "Title")
cb.grouped_bar(cats, groups, "Title", "Y", group_labels=["G1", "G2"])
```

**Theme:** Automatisch dark-professional (#121A2E + Gold), 200 DPI, 16:9.

### 5. PowerPoint MCP Server (37 Tools)
Direkte PPTX-Manipulation via MCP — Alternative zum Build-Script.
Registriert als `ppt`, 37 Tools inkl. `create_presentation`, `add_slide`, `manage_text`, `manage_image`, `add_chart`, `apply_professional_design`.

**Wann MCP statt Build-Script:** Für schnelle Einzeländerungen oder Tests.
**Wann Build-Script:** Für reproduzierbare, versionierte Builds.

### 6. PPTX Builder (`scripts/build_academic_{slug}.py`)
Baut die finale PowerPoint mit python-pptx. Pro Projekt ein eigenes Script.
Bettet Excalidraw-PNGs, Matplotlib-PNGs und Imagen-PNGs als Bilder ein.

### Entscheidungsbaum: Welches Tool wann?

```
Slide-Inhalt bestimmen:
│
├── Struktur-Diagramm (Hierarchie, Flow, Quadrant, Mapping)?
│   └── EXCALIDRAW (Generator oder MCP)
│
├── Daten-Visualisierung (Graph, Balken, Scatter)?
│   └── MATPLOTLIB (ChartBuilder)
│
├── Atmosphärisches Bild (Title, Section, Closing)?
│   └── IMAGEN (generate_image.py)
│
├── Einfacher Text / Zitat / Aufzählung?
│   └── PYTHON-PPTX Shapes (im Build-Script)
│
└── Schnelle Einzeländerung an bestehender PPTX?
    └── POWERPOINT MCP
```

---

## PHASE 0 — Input & Konfiguration

1. **Input lesen:**
   - PDF: `python3 -c "import fitz; doc=fitz.open('$ARGUMENTS'); [print(p.get_text()) for p in doc]"`
   - topic.md: direkt lesen
   - PPTX: `python3 -c "from pptx import Presentation; prs=Presentation('$ARGUMENTS'); [print(s.shapes.title.text if s.shapes.title else '') for s in prs.slides]"`

2. **Style bestimmen:** Falls nicht angegeben → User fragen:
   - `dark-professional` (Navy #121A2E + Gold #F0AB00 — Standard für akademisch)
   - `light-modern` (Weiß + Teal)
   - `minimal` (Reinweiß)

3. **Sprache bestimmen:** Englisch oder Deutsch (aus Input ableiten oder fragen)

---

## PHASE 1 — Inhaltliche Analyse & Slide-Planung

### Schritt 1.1: Paper komplett verstehen
- Kernthese identifizieren
- Argumentationsstruktur erfassen
- Schlüsselzitate extrahieren (max. 3-5 für die gesamte Präsentation)
- Zentrale Diagramme/Konzepte identifizieren

### Schritt 1.2: Slide-Struktur planen

**Pflicht-Slides:**
| # | Typ | Zweck |
|---|-----|-------|
| 1 | title | Titel + Autoren + Imagen-Bild |
| 2 | content | Zentrale Forschungsfrage |
| 3 | content/roadmap | Paper-Struktur / Agenda |
| ... | content | Kernargumente (je 1 Idee/Slide) |
| N-1 | content | Implikationen / Discussion |
| N | closing | Fazit + Kernaussage + Imagen-Bild |

**Section Dividers:** Bei >12 Slides für thematische Blöcke einfügen (mit Imagen-Bild).

**Richtwerte:**
- 10-min Talk → 8-10 Slides
- 15-min Talk → 12-15 Slides
- 20-min Talk → 15-20 Slides
- Seminar (45-min) → 25-35 Slides

### Schritt 1.3: Pro Slide entscheiden — Excalidraw, Imagen oder Text-only?

```
EXCALIDRAW DIAGRAMM wenn:
  → Hierarchie, Taxonomie, Klassifikation
  → Prozess, Zyklus, Feedback-Loop
  → Vergleich / Matrix / 2D-Quadrant
  → Mapping zwischen Konzepten
  → Timeline / Phasen
  → Flowchart / Entscheidungsbaum
  → Tabelle mit wenigen Datenpunkten
  → Anything mit Struktur + Text-Labels

IMAGEN BILD wenn:
  → Title Slide (atmosphärisch, setzt Ton)
  → Section Divider (thematisch, abstrakt)
  → Closing Slide (einprägsam)
  → NICHT für Content-Slides!

KEIN BILD wenn:
  → Reine Definitionen
  → Zitat-Slide
  → Aufzählung die selbsterklärend ist
```

### Schritt 1.4: workspace/slide_structure.md erstellen
```
**Slide N: [Deklarativer Titel]**
**Type:** content | title | section | closing
**Visualization:** excalidraw | imagen | none
**Diagram Type:** hierarchy | cycle | matrix | table | tree | flow | comparison | quadrant | none
**Key Content:** [Stichwörter, max 20 Wörter]
**Speaker Notes:** [Kurzbeschreibung was der Speaker sagt]
```

---

## PHASE 2 — Build (v1)

### Schritt 2.1: Excalidraw-Diagramme generieren

Für jede Slide mit `Visualization: excalidraw`:
1. Eigenes Python-Script oder Funktion in `build_academic_{slug}.py`
2. `ExcalidrawBuilder` verwenden (import aus `scripts/generate_excalidraw.py`)
3. Canvas 1280×720, dark background
4. Export als PNG nach `output/images/{slug}_s{NN}_diagram.png`

**Excalidraw Design-Regeln:**
- Titel-Text: 28pt, Weiß, font_family=5 (Helvetica)
- Label-Text: 16-20pt
- Sublabel-Text: 14pt, gedämpfte Farbe (#C8D6E5)
- Max 6 Elemente pro Diagramm
- Boxen: Fill #1E3050, Stroke in Level-Farbe
- Achsen/Linien: #7A8BA0 (muted)
- Akzente: #F0AB00 (gold)
- Box-Rundung: Excalidraw kann KEINE dezente Rundung bei großen Boxen (`roundness=1/2/3` sind alle zu rund). Für leicht abgerundete Boxen → Pillow verwenden (`ImageDraw.rounded_rectangle` mit `radius=20` bei 2x Scale). Excalidraw `roundness=0` (eckig) als Fallback wenn Pillow nicht nötig. Kreise/Ellipsen bleiben in Excalidraw.
- Labels DIREKT an Elementen, keine separate Legende
- Z-Order beachten: Boxen ÜBER Linien/Pfeilen (Linien zuerst erstellen, Boxen danach → Boxen haben höheren Z-Index)
- Linien/Pfeile IMMER an Box-Kanten ansetzen, NICHT innerhalb der Box enden — Koordinaten berechnen: Box-Rand = box_x + box_w (rechts), box_y + box_h/2 (Mitte vertikal) etc.
- Linien/Pfeile dürfen NIEMALS Text kreuzen — wenn eine Linie durch Text läuft, Layout umbauen (Routing ändern, Elemente umpositionieren, oder Linie um Text herum führen)
- Trennlinien zwischen Überschrift und Folgetext innerhalb einer Box sind OK (wirkt als visuelle Trennung). ABER: Folgetext/Body-Text benachbarter Boxen darf NIEMALS ineinander überlaufen. Vor dem Export prüfen: Passt der gesamte Text (inkl. längster Wörter) in die Box-Breite? Wenn nicht → Text kürzen, Font verkleinern, oder Box verbreitern.
- Bei hierarchischen Layouts (z.B. Steps in einer Gruppe): KEINE separate Box auf eine größere Box draufsetzen. Stattdessen die große Box mit einem farbig gefüllten Header-Bereich versehen (gleiche Breite wie die Box) und den übergeordneten Step/Titel dort reinschreiben. Wirkt sauberer und integrierter.

### Schritt 2.2: Imagen-Bilder generieren (Title, Section, Closing)

```bash
python3 scripts/generate_image.py \
  --slide N --prompt "..." --version 1 --slide-type [title|section|closing]
```

**Image-Prompts IMMER:**
- Auf Englisch
- Lichtstimmung nennen
- Perspektive nennen
- "absolutely no text, no letters, no words, no watermarks"
- Zum akademischen Ton passend

### Schritt 2.3: PPTX Builder erstellen

Erstelle `scripts/build_academic_{slug}.py` mit:
- Einer Funktion pro Slide (`slide_01_title`, `slide_02_xxx`, ...)
- Excalidraw-PNGs als Bilder einbetten (volle Slide-Breite oder rechte Hälfte)
- Imagen-PNGs für Title/Section/Closing
- Einfache Text-Slides mit python-pptx Shapes (wo kein Bild nötig)

**Design-Regeln (STRIKT einhalten):**

| Element | Minimum | Empfohlen |
|---------|---------|-----------|
| Titel-Font | 28pt | 32pt |
| Bullet-Font | 20pt | 24pt |
| Label-Font | 14pt | 16pt |
| Footer-Font | 9pt | 10pt |
| Elemente/Slide | — | max. 6 |
| Wörter/Slide | — | max. 20 |
| Bullets/Slide | — | max. 5 |
| Farben | — | max. 4 |

**Pflicht-Elemente pro Slide:**
- Deklarativer Titel (Kernaussage, NICHT generisch wie "Results")
- Footer mit Slide-Nummer + Quellenverweis
- Konsistentes Farbschema
- Speaker Notes

**Verboten:**
- Ganze Sätze (außer Zitate)
- Dekorative Bilder ohne Informationswert
- Animationen
- Comic Sans, WordArt
- Logos auf jeder Slide (nur Title + Closing)
- ALL CAPS für Fließtext
- Dekorative Linien/Striche die teils im Bild, teils als PPTX-Shape existieren → INKONSISTENZ! Entscheide dich: entweder NUR im Bild ODER nur als PPTX-Shape, niemals gemischt
- Text der über Box-/Shape-Grenzen hinausragt — IMMER vorher prüfen ob der Text in die Box passt (Textlänge × Font-Größe vs. Box-Breite)

### Schritt 2.4: v1 bauen

```bash
python3 scripts/build_academic_{slug}.py
```

Output: `output/presentations/{slug}_v1.pptx`

---

## PHASE 3 — Bull & Bear Critique (Runde 1)

### BULL CASE — Pro Slide:
- Was macht diese Slide stark?
- Ist die Kernbotschaft sofort klar?
- Würde ein Professor nicken?
- Ist die Visualisierung informativ (nicht nur hübsch)?

### BEAR CASE — Pro Slide:
- Ist diese Slide wirklich nötig? Könnte sie weg?
- Kann ein Zuhörer den Inhalt in <5 Sekunden erfassen?
- Ist das Bild/Diagramm nur Dekoration?
- Gibt es Cognitive Load Probleme?
  - Split Attention (Label weit weg vom Diagramm)?
  - Redundanz (Text = was der Speaker sagt)?
  - Zu viele Elemente (>6)?
- Fehlt eine Quellenangabe?
- Font zu klein? (<20pt Content, <14pt Labels)
- Zu viel Text? (>20 Wörter, ganze Sätze?)
- Würde ein Student OHNE Vorwissen verstehen worum es geht?
- Gibt es dekorative Elemente (Linien, Striche, Rahmen) die inkonsistent sind — teils im Bild, teils als PPTX-Shape?
- Ragt Text über die Grenzen seiner Box/Shape hinaus?
- Sind Pfeile/Linien hinter Boxen versteckt statt darunter (Z-Order falsch)?
- Enden Verbindungslinien innerhalb von Boxen statt an deren Kanten/Rändern?
- Kreuzen Linien/Pfeile irgendwo Text? → Layout umbauen!

### BEAR CASE — Gesamtpräsentation:
- Ist der rote Faden erkennbar?
- Fehlt ein wichtiges Konzept aus dem Paper?
- Ist die Slide-Reihenfolge logisch?
- Sind die Übergänge klar?
- Stimmt die Balance? (nicht 80% Theorie, 20% Ergebnisse)

### Output: workspace/critique_v1.md
Für jede Slide: Bull Score (1-5), Bear Score (1-5), konkrete Verbesserungen.

---

## PHASE 4 — Überarbeitung (v2)

Basierend auf critique_v1.md:

1. **Inhaltliche Fixes:** Titel verbessern, Bullets kürzen, Slides mergen/splitten
2. **Visuelle Fixes:** Font-Größen, Diagramm-Verbesserungen, Spacing
3. **Excalidraw-Fixes:** Layout anpassen, Labels verschieben, Elemente reduzieren
4. **Imagen-Fixes:** Nur regenerieren wenn inhaltlich falsch (nicht nur "schöner")

Output: `output/presentations/{slug}_v2.pptx`

---

## PHASE 5 — Bull & Bear Critique (Runde 2)

Gleiche Methodik wie Phase 3, aber STRENGER:
- Wurde jedes Problem aus Runde 1 behoben?
- Neue Probleme durch die Überarbeitung entstanden?
- Final-Check gegen ALLE Regeln aus dem Regelwerk

### Output: workspace/critique_v2.md

---

## PHASE 6 — Final Polish (v3)

Letzte Überarbeitung basierend auf critique_v2.md.
Fokus auf:
- Pixel-perfekte Ausrichtung
- Konsistente Abstände
- Footer auf allen Slides
- Speaker Notes vervollständigen

Output: `output/presentations/{slug}_v3.pptx`

---

## PHASE 7 — Final Report

Erstelle workspace/final_report.md:

```markdown
# Scientific Presentation — Final Report

## Empfohlene Version: v3
## Scores: v1 → v2 → v3
## Slide-Übersicht (Typ, Visualisierung, Score)
## Was die Kritikschleifen gebracht haben
## Bekannte Limitierungen
```

Melde dem User:
- Pfad zur finalen .pptx
- Anzahl Slides
- Score-Vergleich v1 → v2 → v3
- Welche Slides Imagen-Bilder haben vs. Excalidraw-Diagramme

---

## CHECKLISTE (vor Abgabe jeder Version)

- [ ] Jede Slide hat nur 1 Idee
- [ ] Max. 6 Elemente pro Slide
- [ ] Titel = Kernaussage (nicht "Results" oder "Methods")
- [ ] Max. 20 Wörter pro Slide, keine ganzen Sätze
- [ ] Alle Fonts ≥ 20pt (Content), ≥ 14pt (Labels), ≥ 9pt (Footer)
- [ ] Keine dekorativen Bilder — jedes Bild hat Informationswert
- [ ] Quellenangaben bei fremden Inhalten
- [ ] Footer mit Slide-Nummer auf jeder Slide (außer Title)
- [ ] Konsistentes Farbschema (max. 4 Farben)
- [ ] Genug Whitespace
- [ ] Keine Inkonsistenz bei dekorativen Elementen (Linien, Striche, Rahmen) — entweder im Bild ODER als PPTX-Shape, nie gemischt
- [ ] Kein Text ragt über Box-/Shape-Grenzen hinaus — bei langen Strings Font verkleinern oder Box verbreitern
- [ ] Excalidraw-Diagramme: Labels direkt am Element
- [ ] Excalidraw-Diagramme: Verbindungslinien zwischen zusammengehörigen Elementen
- [ ] Excalidraw-Diagramme: Pfeile/Linien IMMER VOR (unter) den Boxen — nie hinter/über den Boxen gerendert
- [ ] Excalidraw-Diagramme: Linien/Pfeile enden an Box-Kanten (Verbindungspunkte), NICHT innerhalb der Boxen
- [ ] Excalidraw-Diagramme: Keine Linie/Pfeil kreuzt Text — bei Überschneidung Layout korrigieren
- [ ] Speaker Notes für jede Slide
- [ ] Excalidraw-PNGs in ausreichender Auflösung (scale=2 minimum)
