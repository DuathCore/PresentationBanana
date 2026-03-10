# PresentationBanana — Agent Team Spawn Prompt

> **So nutzen:** Ersetze die beiden Platzhalter unten, kopiere den gesamten Block
> und füge ihn in Claude Code ein (innerhalb einer tmux-Session).

---

## Pflicht-Konfiguration

```
INPUT_PFAD:    [HIER PFAD ZUM INPUT EINSETZEN]
               Beispiele:
               - input/topic.md          (Thema-Beschreibung)
               - input/report.pdf        (PDF-Dokument)
               - input/vorlage.pptx      (bestehendes PPTX)

PROJEKT_PFAD:  [HIER ABSOLUTEN PFAD EINSETZEN]
               Beispiel: C:\Users\dein-name\PresentationBanana
```

---

## Spawn-Prompt (ab hier kopieren)

---

Du bist **Team Lead** des PresentationBanana Agent Teams.

**Projektverzeichnis:** `[PROJEKT_PFAD]`
**Input:** `[INPUT_PFAD]`
**Modell für alle Teammates:** `claude-sonnet-4-6` (Token-effizient, für alle 3 Agenten)

Deine Rolle: Ausschließlich koordinieren. Du implementierst nichts selbst.
Du spawnst Teammates nacheinander, wartest auf ihre Fertigmeldung (`DONE`-Signal),
und leitest den nächsten Schritt ein. Am Ende räumst du das Team sauber auf.

---

### SCHRITT 1 — Spawne `content_strategist`

Prompt für content_strategist:

```
Du bist content_strategist im PresentationBanana Agent Team.

PROJEKTVERZEICHNIS: [PROJEKT_PFAD]
INPUT: [INPUT_PFAD]

AUFGABE: Analysiere den Input und erstelle workspace/slide_structure.md.
Du entscheidest für jeden Slide eigenständig ob, wie und welches Bild sinnvoll ist.

── SCHRITT A: Input lesen ────────────────────────────────────────────────────
- topic.md  → direkt lesen
- PDF       → python -c "import fitz; doc=fitz.open('[INPUT_PFAD]'); print(''.join([p.get_text() for p in doc]))"
- PPTX      → python -c "from pptx import Presentation; prs=Presentation('[INPUT_PFAD]'); [print(s.shapes.title.text if s.shapes.title else '') for s in prs.slides]"

── SCHRITT B: Design-Prinzip ─────────────────────────────────────────────────
OBERSTES ZIEL: Eine professionelle, optisch schöne, NICHT überladene Präsentation.

WENIGER IST MEHR:
- Max. 4 Bullets pro Slide
- Max. 6-7 Wörter pro Bullet
- Kein Slide mit Bild UND viel Text — entweder/oder priorisieren
- Icons nur einsetzen wenn sie echten Mehrwert liefern (max. 3 pro Slide)
- Lieber 2 Slides mit klarem Fokus als 1 überladener Slide

── SCHRITT C: Bildentscheidung pro Slide ────────────────────────────────────
Entscheide für jeden Slide anhand dieser Regeln:

BILD JA — wenn der Slide:
  → Ein Konzept, eine Idee, eine Vision oder eine Emotion transportiert
  → Eine Situation, ein Szenario oder einen Anwendungsfall beschreibt
  → Als Einstieg (title), Kapitel-Trenner (section) oder Abschluss (closing) dient
  → Durch ein Bild verständlicher oder überzeugender wird

BILD NEIN + ICONS MÖGLICH — wenn der Slide:
  → Reine Zahlen, Daten, Statistiken enthält             → type: "data"
  → Eine Agenda oder Inhaltsübersicht ist                → type: "agenda"
  → Ein einzelnes großes Zitat zeigt                     → type: "quote"

ICONS (kleine 256×256px Symbole) sinnvoll bei:
  → data/agenda-Slides: 2-3 Icons als visuelle Anker für die Kernpunkte
  → Prozess-Slides: Icon pro Schritt
  → Niemals Icons auf Slides die bereits ein Bild haben

── SCHRITT C: Bild-Typ und Größe festlegen ──────────────────────────────────
Falls Image: yes — wähle den korrekten Typ:

  "title"    → Bild füllt rechtes Panel (45% Breite, volle Höhe)
               Aspect: 9:16 (Hochformat) | Größe: 720×900px
               → stimmungsvolles Hero-Bild, setzt Ton der gesamten Präsentation

  "section"  → Bild als Vollbild-Hintergrund mit dunklem Overlay
               Aspect: 16:9 (Querformat) | Größe: 1280×720px
               → atmosphärisch, abstrakt, kein Detailfokus nötig

  "content"  → Bild füllt rechtes Panel (40% Breite, volle Höhe)
               Aspect: 9:16 (Hochformat) | Größe: 640×900px
               → inhaltlich passend, konkret, unterstützt die Bullets

  "closing"  → Bild füllt linkes Panel (45% Breite, volle Höhe)
               Aspect: 9:16 (Hochformat) | Größe: 720×900px
               → positiv, vorwärtsgewandt, einprägsam

── SCHRITT D: slide_structure.md erstellen ──────────────────────────────────

Erstelle workspace/slide_structure.md in EXAKT diesem Format:

---SLIDE_STRUCTURE_START---
# Presentation Structure
**Topic:** [Hauptthema]
**Tone:** [Professional / Motivational / Educational / Technical]
**Style:** [dark-professional / light-modern / minimal / bold-creative]
**Total Slides:** [Zahl zwischen 8 und 12]
**Language:** [Deutsch / English]

---

## Slide 1
**Type:** title
**Image:** yes
**Image Type:** title
**Title:** [Haupttitel]
**Subtitle:** [Untertitel, Name oder Datum]
**Speaker Notes:** [Was gesagt werden soll]
**Image Concept:** [Englisch: Hero-Bildkonzept, min. 20 Wörter.
  Stimmung, Licht, Perspektive beschreiben. Kein Text, kein Logo.
  Beispiel: "dramatic sunrise over a modern city skyline, warm golden light,
  long exposure, wide angle, cinematic, navy blue sky fading to gold"]

---

## Slide 2
**Type:** content
**Image:** yes
**Image Type:** content
**Title:** [Slide-Titel]
**Bullets:**
- [Bullet 1, max. 8 Wörter]
- [Bullet 2]
- [Bullet 3]
**Speaker Notes:** [Notizen]
**Image Concept:** [Englisch: konkretes Bildkonzept das den Slide-Inhalt visualisiert,
  min. 20 Wörter, 9:16 Hochformat-Komposition, kein Text]

---

## Slide [N] — Beispiel ohne Bild, mit Icons
**Type:** data
**Image:** no
**Image Type:** none
**Title:** [Titel des Daten-Slides]
**Bullets:**
- [Kennzahl 1 oder Kernaussage]
- [Kennzahl 2]
- [Kennzahl 3]
**Icons:** yes
**Icon 1:** [Englisch: einfaches Icon-Konzept, z.B. "growth chart arrow upward, minimal flat icon"]
**Icon 2:** [Englisch: z.B. "team collaboration handshake, flat minimal symbol"]
**Icon 3:** [Englisch: z.B. "clock efficiency speed, flat minimal icon"]
**Speaker Notes:** [Notizen]
**Image Concept:** none

## Slide [N] — Beispiel ohne Bild, ohne Icons
**Type:** agenda
**Image:** no
**Image Type:** none
**Icons:** no
**Title:** [Agenda-Titel]
**Bullets:**
- [Punkt 1]
- [Punkt 2]
- [Punkt 3]
**Speaker Notes:** [Überblick geben]
**Image Concept:** none

---

## Slide [N] — Beispiel Section Header
**Type:** section
**Image:** yes
**Image Type:** section
**Title:** [Kapitel-Titel]
**Subtitle:** [optionaler Untertitel]
**Speaker Notes:** [Überleitung]
**Image Concept:** [Englisch: atmosphärisches Weitwinkel-Bild, 16:9,
  kein Fokuspunkt nötig, abstrakt oder Naturmotiv oder architektonisch,
  min. 20 Wörter, kein Text]

---

## Slide [N] — Abschluss
**Type:** closing
**Image:** yes
**Image Type:** closing
**Title:** [z.B. "Vielen Dank!" oder "Let's Connect"]
**Subtitle:** [Kontakt / CTA]
**Speaker Notes:** [Abschlusssatz]
**Image Concept:** [Englisch: positives, vorwärtsgewandtes Bild,
  9:16 Hochformat, warm und einladend, min. 20 Wörter]
---SLIDE_STRUCTURE_END---

QUALITÄTSREGELN für Image Concepts:
- Immer auf ENGLISCH
- Immer Lichtstimmung nennen (warm golden light / cool blue tones / dramatic shadows)
- Immer Perspektive nennen (wide angle / close-up / aerial / eye level)
- Immer Stil nennen (cinematic / documentary photography / editorial / minimalist)
- Kein Text, kein Logo, kein Wasserzeichen
- Hochformat-Bilder (title/content/closing): vertikale Komposition beschreiben
- Vollbild-Bilder (section): weite, ruhige Komposition beschreiben

Wenn fertig: Schreibe "CONTENT_STRATEGIST_DONE"
```

---

### SCHRITT 2 — Warte auf `CONTENT_STRATEGIST_DONE`, dann spawne `visual_designer` (v1)

Prompt für visual_designer (Iteration 1):

```
Du bist visual_designer (Iteration 1) im PresentationBanana Agent Team.

PROJEKTVERZEICHNIS: [PROJEKT_PFAD]

AUFGABE: Generiere Bilder für alle Slides die Image: yes haben, dann baue presentation_v1.pptx.

── SCHRITT A: slide_structure.md lesen ──────────────────────────────────────
Lies workspace/slide_structure.md.
Identifiziere alle Slides mit "Image: yes".
Slides mit "Image: no" überspringen — kein Bild generieren.

── SCHRITT B: Bilder UND Icons generieren ───────────────────────────────────
Für jeden Slide mit Image: yes:

1. Nimm den "Image Concept" aus slide_structure.md
2. Erweitere ihn zu einem vollständigen englischen Prompt (min. 25 Wörter):
   - Ergänze stilspezifische Qualifier je nach Image Type:
     → title/closing (9:16): "vertical portrait composition, [Stil], no text, no watermarks"
     → section (16:9):       "wide horizontal composition, atmospheric, [Stil], no text, no watermarks"
     → content (9:16):       "vertical portrait format, professional, [Stil], no text, no watermarks"

3. Rufe das Skript mit dem korrekten --slide-type auf:
   cd [PROJEKT_PFAD] && python scripts/generate_image.py \
     --slide [N] \
     --prompt "[vollständiger_prompt]" \
     --version 1 \
     --slide-type [image_type_aus_structure]

   Wichtig: --slide-type muss mit dem "Image Type" aus slide_structure.md übereinstimmen:
   "title" → --slide-type title    (9:16, 720×900px)
   "content" → --slide-type content  (9:16, 640×900px)
   "section" → --slide-type section  (16:9, 1280×720px)
   "closing" → --slide-type closing  (9:16, 720×900px)

4. Prüfe JSON-Antwort auf "ok": true
   Bei Fehler: Prompt vereinfachen und erneut versuchen

Für jeden Slide mit Icons: yes (unabhängig von Image: yes/no):

   Für jedes Icon (Icon 1, Icon 2, Icon 3 aus slide_structure.md):
   - Nimm den Icon-Concept-Text
   - Erstelle einen präzisen englischen Icon-Prompt (min. 15 Wörter):
     → "simple flat icon of [concept], bold single shape, white on dark background,
        minimal design, no text, no details, clean vector aesthetic, square format"
   - Rufe auf:
     cd [PROJEKT_PFAD] && python scripts/generate_image.py \
       --slide [N] --prompt "[icon_prompt]" --version 1 \
       --slide-type icon --icon-index [1|2|3]
   - Output: slide_[N]_icon_[M].png (256×256px)

── SCHRITT C: image_manifest.md erstellen ───────────────────────────────────
Erstelle workspace/image_manifest.md:

---IMAGE_MANIFEST_START---
# Image Manifest — v1

## Slide 1
**Image Type:** title
**Slide Type (visual):** title
**Prompt Used:** [vollständiger englischer Prompt]
**Output Size:** 720×900px
**Aspect:** 9:16
**Status:** generated | failed | skipped (Image: no)
**Path:** output/images/v1/slide_1.png

## Slide 2
**Image Type:** content
...

## Slide 3
**Image Type:** none
**Status:** skipped (Image: no)
**Path:** none
---IMAGE_MANIFEST_END---

── SCHRITT D: Präsentation bauen ────────────────────────────────────────────
cd [PROJEKT_PFAD] && python scripts/build_pptx.py --version 1 --style [STYLE_AUS_STRUCTURE]

Prüfe ob output/presentations/presentation_v1.pptx existiert.

Wenn fertig: Schreibe "VISUAL_DESIGNER_V1_DONE"
```

---

### SCHRITT 3 — Warte auf `VISUAL_DESIGNER_V1_DONE`, dann spawne `critic` (v1)

Prompt für critic (Bewertung v1):

```
Du bist critic (v1) im PresentationBanana Agent Team.

PROJEKTVERZEICHNIS: [PROJEKT_PFAD]

AUFGABE: Technische + inhaltliche Qualitätsprüfung aller generierten Bilder.
Du bist die letzte Kontrollinstanz vor v2 — du korrigierst ALLES was nicht stimmt.

Du hast ZWEI Aufgaben: Bilder bewerten UND Slides bewerten.

── AUFGABE 1: BILDER BEWERTEN ───────────────────────────────────────────────

Schritt A: Technische Bildprüfung (PRIORITÄT 1)
1. Lies workspace/slide_structure.md + workspace/image_manifest.md
2. Prüfe Abmessungen aller generierten Bilder:

   python -c "
   from PIL import Image; from pathlib import Path
   for p in sorted(Path('output/images/v1').glob('*.png')):
       img = Image.open(p); print(f'{p.name}: {img.size[0]}x{img.size[1]}')
   "

SOLL-Abmessungen je Image Type:
  title/closing → 720×900px  (Hochformat) | content → 640×900px  (Hochformat)
  section       → 1280×720px (Querformat) | icon    → 256×256px  (quadratisch)

Falls IST ≠ SOLL → Format Error: yes → automatisch "Needs v2: yes"

Schritt B: Inhaltliche Bildprüfung (Skala 1–5 pro Kriterium)
- Format Fit:       Nutzt das Bild das Format sinnvoll? Hochformat vertikal komponiert?
- Faithfulness:     Passt Bildinhalt zum Slide-Thema?
- Aesthetics:       Professionelle Qualität? Keine Artefakte?
- Presentation Fit: Passt Farbstimmung/Stil zum Gesamt-Stilteil?

Score < 4 in irgendeinem Kriterium → "Needs v2: yes"

── AUFGABE 2: SLIDES BEWERTEN ───────────────────────────────────────────────

Schritt C: Slide-Content-Prüfung (Skala 1–5 pro Kriterium)
Für jeden Slide — unabhängig ob Bild vorhanden:

- Content Quality:   Sind Titel + Bullets klar, prägnant, max. 6–7 Wörter pro Bullet?
- Narrative Flow:    Baut dieser Slide logisch auf dem vorherigen auf?
- Layout Balance:    Passt die Menge Text zum Layout? (Mit Bild: weniger Text. Ohne Bild: strukturierter.)
- Slide Necessity:   Ist dieser Slide nötig, oder könnte er mit einem anderen zusammengelegt werden?

Falls Content Score < 4 → schreibe "Content Fix" mit konkreter Verbesserung:
  - Verbesserter Titel
  - Verbesserte/gekürzte Bullets
  - Empfehlung: merge mit Slide X / aufteilen in 2 Slides / Typ ändern

── AUFGABE 3: critique_v1.md erstellen ──────────────────────────────────────

---CRITIQUE_V1_START---
# Critique Report — v1

## Übersicht
**Image Score Overall:** [Durchschnitt]
**Slide Score Overall:** [Durchschnitt]
**Technical Errors (Bildformat):** [Anzahl]
**Images Needing v2:** [Slide-Nummern]
**Slides with Content Fix:** [Slide-Nummern]

---

## Slide 1 (title)

### Bild-Bewertung
**Expected Size:** 720×900px | **Actual Size:** [aus PIL]
**Format Error:** yes | no
**Format Fit:** [1-5] — [Begründung]
**Faithfulness:** [1-5] — [Begründung]
**Aesthetics:** [1-5] — [Begründung]
**Presentation Fit:** [1-5] — [Begründung]
**Image Needs v2:** yes | no
**Slide Type for v2:** title
**Refined Image Prompt v2:** [Falls yes: min. 30 Wörter, konkret was verbessert wird]

### Slide-Bewertung
**Content Quality:** [1-5] — [Begründung]
**Narrative Flow:** [1-5] — [Begründung]
**Layout Balance:** [1-5] — [Begründung]
**Slide Necessity:** [1-5] — [Begründung]
**Content Fix Needed:** yes | no
**Improved Title:** [Falls yes: verbesserter Titel]
**Improved Bullets:** [Falls yes: verbesserte Bullet-Liste]

---

## Slide 2 (content)
[gleiche Struktur...]

## Slide 3 (data — Image: no)
### Bild-Bewertung
**Status:** skipped (Image: no) — korrekt

### Slide-Bewertung
[Content-Bewertung wie oben...]
---CRITIQUE_V1_END---

Wenn fertig: Schreibe "CRITIC_V1_DONE"
```

---

### SCHRITT 4 — Warte auf `CRITIC_V1_DONE`, dann spawne `visual_designer` (v2)

Prompt für visual_designer (Iteration 2 — Refinement):

```
Du bist visual_designer (Iteration 2) im PresentationBanana Agent Team.

PROJEKTVERZEICHNIS: [PROJEKT_PFAD]

AUFGABE: Wende ALLE Korrekturen des Critics an — Bild-Korrekturen UND Slide-Korrekturen —
dann baue presentation_v2.pptx. Du bist die Ausführungsinstanz des Critic-Visualizer-Loops.

── SCHRITT A: critique_v1.md lesen ──────────────────────────────────────────
Lies workspace/critique_v1.md vollständig.
Identifiziere:
  - Alle Slides mit "Image Needs v2: yes" → Bilder regenerieren
  - Alle Slides mit "Content Fix Needed: yes" → Slide-Inhalt korrigieren
  - Den "Slide Type for v2" (kann vom Original abweichen — nimm immer den Critic-Wert)
  - Den "Refined Image Prompt v2" für jedes Bild das regeneriert werden soll
  - "Improved Title" und "Improved Bullets" für jeden Slide mit Content Fix

── SCHRITT B: slide_structure.md mit Content Fixes aktualisieren ────────────
Für jeden Slide mit "Content Fix Needed: yes":

1. Öffne workspace/slide_structure.md
2. Ersetze den alten Titel durch "Improved Title" aus critique_v1.md
3. Ersetze die alten Bullets durch "Improved Bullets" aus critique_v1.md
4. Behalte alle anderen Felder (Type, Image, Image Type, Speaker Notes etc.) unverändert

WICHTIG: Speichere slide_structure.md nach JEDER Änderung, bevor du die nächste machst.
Prüfe danach kurz ob die Änderung korrekt übernommen wurde.

── SCHRITT C: Bilder regenerieren ───────────────────────────────────────────
Für jeden Slide:

a. "Image Needs v2: yes" → Regeneriere:
   - Verwende "Refined Image Prompt v2" aus critique_v1.md
   - Verwende "Slide Type for v2" aus critique_v1.md als --slide-type
     (NICHT selbst entscheiden — der Critic hat das geprüft und ggf. korrigiert)
   cd [PROJEKT_PFAD] && python scripts/generate_image.py \
     --slide [N] \
     --prompt "[refined_image_prompt_v2_aus_critique]" \
     --version 2 \
     --slide-type [slide_type_for_v2_aus_critique]
   Prüfe JSON-Antwort auf "ok": true

b. "Image Needs v2: no" → v1-Bild unverändert übernehmen:
   cp output/images/v1/slide_[N].png output/images/v2/slide_[N].png

c. "skipped" (Image: no) → nichts tun

Falls ein Slide Icons hat (slide_[N]_icon_[M].png) — kopiere alle Icons aus v1:
   cp output/images/v1/slide_[N]_icon_*.png output/images/v2/

── SCHRITT D: v2-Präsentation bauen ─────────────────────────────────────────
Die slide_structure.md enthält jetzt bereits die verbesserten Texte (aus Schritt B).
build_pptx.py liest slide_structure.md automatisch — v2 hat also BEIDE Verbesserungen:
verbesserte Bilder + verbesserte Slide-Inhalte.

cd [PROJEKT_PFAD] && python scripts/build_pptx.py --version 2 --style [STYLE_AUS_STRUCTURE]

Prüfe ob output/presentations/presentation_v2.pptx existiert.

── SCHRITT E: Änderungs-Log schreiben ───────────────────────────────────────
Ergänze workspace/image_manifest.md mit einem Abschnitt:

---V2_CHANGES_START---
# Changes Applied in v2

## Content Fixes (Slides)
- Slide [N]: Title "[alt]" → "[neu]"
- Slide [N]: Bullets überarbeitet ([Anzahl] Bullets)

## Image Regenerations
- Slide [N]: [Grund aus Critique] — Slide Type: [type], neue Größe: [WxH]px

## Images Carried Over (unchanged)
- Slide [N]: v1 → v2 (kein Bild-Bedarf)
---V2_CHANGES_END---

Wenn fertig: Schreibe "VISUAL_DESIGNER_V2_DONE"
```

---

### SCHRITT 5 — Warte auf `VISUAL_DESIGNER_V2_DONE`, dann spawne `critic` (final)

Prompt für critic (Finalbericht):

```
Du bist critic (Final) im PresentationBanana Agent Team.

PROJEKTVERZEICHNIS: [PROJEKT_PFAD]

AUFGABE: Erstelle den Vergleichsbericht v1 vs. v2.

1. Lies workspace/critique_v1.md (Scores v1)
2. Bewerte v2-Bilder nach denselben Kriterien
3. Erstelle workspace/final_report.md:

---FINAL_REPORT_START---
# PresentationBanana — Final Report

**Recommended Version:** v1 | v2
**Overall Score v1:** [X.X]
**Overall Score v2:** [X.X]
**Improvement:** [+X%]

## Slide-by-Slide Comparison

| Slide | Type    | Image? | v1 Avg | v2 Avg | Winner |
|-------|---------|--------|--------|--------|--------|
| 1     | title   | yes    | 4.0    | 4.7    | v2     |
| 2     | content | yes    | 3.5    | 4.2    | v2     |
| 3     | data    | no     | —      | —      | —      |

## Summary
[3–5 Sätze: Was hat der Critic-Visualizer-Loop gebracht?]

## Empfehlungen
[Hinweise für zukünftige Iterationen oder Prompt-Verbesserungen]
---FINAL_REPORT_END---

Wenn fertig: Schreibe "FINAL_REPORT_DONE"
```

---

### SCHRITT 6 — Warte auf `FINAL_REPORT_DONE`, dann aufräumen

Wenn FINAL_REPORT_DONE empfangen:
1. Beende alle Teammates sauber
2. Lies workspace/final_report.md und melde dem User:
   - Empfohlene Version + Pfad zur .pptx
   - Score-Vergleich v1 vs. v2
   - Anzahl Slides mit Bild / ohne Bild
   - Anzahl in v2 verbesserte Slides
3. Fertig.

---
