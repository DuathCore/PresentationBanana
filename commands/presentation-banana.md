---
name: presentation-banana
description: >
  Erstellt eine professionelle PowerPoint-Präsentation mit KI-generierten Bildern
  via Gemini Imagen 3. Vollständiger Critic-Visualizer-Loop: Inhaltsanalyse →
  Bilderstellung v1 → Critic (Bilder + Slides) → Verbesserung v2 → Finalbericht.
  Trigger: wenn der User eine Präsentation, Powerpoint, PPTX oder Slides erstellen möchte.
---

# PresentationBanana

Du führst alle Schritte selbst durch — sequenziell, ohne Teammates.
Projektverzeichnis: `C:\Users\marek\KI  Champions  wissens DB\06_PresentationBanana`

---

## Schritt 1 — Konfiguration erfassen

### 1.1 Input
Falls nicht angegeben, frage: "Was soll die Basis der Präsentation sein?"
- Thema/Text direkt, PDF-Pfad, oder PPTX-Pfad

### 1.2 Stil (PFLICHT — niemals überspringen)

Zeige diese Auswahl und warte auf Antwort:

```
Welchen visuellen Stil soll die Präsentation haben?

1. dark-professional  → Navy + Gold        (Pitches, Investoren, Konferenzen)
2. light-modern       → Weiß + Teal        (Produkt, Tech, Startups)
3. minimal            → Weiß + Schwarz     (Design, Architektur, Kreativ)
4. bold-creative      → Schwarz + Orange   (Marketing, Events, Sales)
5. passend zum Thema  → Claude wählt automatisch den besten Stil
6. eigene Eingabe     → z.B. "dunkel mit rotem Akzent" oder Hex-Farben
```

Bei Option 5: Analysiere Thema und Ton des Inputs und wähle den passendsten der 4 Stile.
Erkläre kurz warum (1 Satz).

Bei Option 6: User gibt freien Text ein. Mappe ihn auf den nächstpassenden der 4 Stile.
Wenn unklar, kurz nachfragen.

### 1.3 Weitere Parameter
- Slide-Anzahl: Default "passend zum Thema" — Claude bestimmt die optimale Anzahl (8–12) anhand des Inhalts. Nur wenn der User explizit eine Zahl nennt, diese verwenden.
- Sprache: Default Deutsch

Kurze Zusammenfassung zeigen + Bestätigung abwarten.

---

## Schritt 2 — Rolle: content_strategist

Analysiere Input, erstelle `workspace/slide_structure.md`.

### Kernprinzipien (Leitfaden für gute Präsentationen):

**Inhalt:**
- **Eine Kernaussage pro Folie** — der Titel formuliert die Botschaft, Bullets belegen sie
- **Narrativstruktur wählen:** Problem → Analyse → Lösung | These → Beleg → Fazit | Situation → Complication → Resolution
- **Stichwörter, kein Fließtext** — die Folie ergänzt den Sprecher, ersetzt ihn nicht
- Erste Folie weckt Interesse, letzte bleibt im Gedächtnis
- **Vollständig wenn nichts mehr weggelassen werden kann** — nicht wenn nichts mehr hinzuzufügen ist

**Design:**
- Weißraum ist kein verschwendeter Platz — überladene Folien wirken unsicher
- Konsistente Bildsprache über alle Folien (gleiche Farbtemperatur, Stimmung, Stil)

### Input lesen:
```bash
# PDF:
python -c "import fitz; doc=fitz.open('[PDF_PFAD]'); print(''.join([p.get_text() for p in doc]))"

# PPTX:
python -c "from pptx import Presentation; prs=Presentation('[PPTX_PFAD]'); [print(s.shapes.title.text if s.shapes.title else '') for s in prs.slides]"
```

### Bildentscheidung pro Slide:

**BILD JA (content, 9:16)** wenn Slide: Konzept + Bullet-Text kombiniert — Bild unterstützt rechts
**BILD ZENTRAL (visual, 16:9)** wenn Slide: Ein Bild erklärt besser als Bullets — Diagramm, Vergleich, Metapher, Prozessablauf. Kein Bullet-Text, nur Titel + Bild + optionale Caption.
**BILD NEIN + ICONS MÖGLICH** wenn Slide: reine Daten, Agenda, Zitat → type: data/agenda/quote

**Faustregel für `visual`:**
- Würde eine Infografik / ein Schema die Aussage direkter vermitteln als 4 Bullets?
- Kann ein visueller Vergleich das Konzept erklären (z.B. "A vs B", Zeitlinie, Kreislauf)?
- Dann → `visual`, kein Bullet-Text, stattdessen eine präzise Image Concept Beschreibung als Erklärbild

### Bild-Typen:
| Image Type | Aspect | Zielgröße  | Layout                                        |
|------------|--------|------------|-----------------------------------------------|
| `title`    | 9:16   | 720×900px  | Rechtes Panel Titelfolie                      |
| `content`  | 9:16   | 640×900px  | Rechtes Panel Inhaltsfolie                    |
| `visual`   | 16:9   | 1280×720px | Zentrales Erklärbild — ersetzt Bullet-Text    |
| `section`  | 16:9   | 1280×720px | Vollbild Kapitel-Trenner (Image als BG)       |
| `closing`  | 9:16   | 720×900px  | Linkes Panel Abschlussfolie                   |
| `icon`     | 1:1    | 256×256px  | Symbol für data/agenda-Slides                 |

### Design-Prinzip WENIGER IST MEHR:
- Max. 4 Bullets/Slide, max. 6–7 Wörter/Bullet
- Kein Slide mit Bild UND viel Text — entweder/oder
- Icons nur wenn echter Mehrwert (max. 3/Slide, nie zusammen mit Bild)
- Weißraum bewusst nutzen — nicht jeden Pixel füllen
- Icons: immer gleicher Stil innerhalb einer Präsentation (Flat, Outline oder Filled — niemals mischen)

### Format workspace/slide_structure.md:
```
---SLIDE_STRUCTURE_START---
# Presentation Structure
**Topic:** [Thema]
**Tone:** [Professional / Motivational / Educational / Technical]
**Style:** [dark-professional / light-modern / minimal / bold-creative]
**Total Slides:** [optimal für das Thema, typisch 8-12]
**Language:** [Deutsch / English]

---

## Slide 1
**Type:** title
**Image:** yes
**Image Type:** title
**Title:** [Haupttitel]
**Subtitle:** [Untertitel]
**Speaker Notes:** [Notizen]
**Image Concept:** [Englisch, min. 20 Wörter, Licht + Perspektive + Stil, kein Text, kein Logo]

---

## Slide [N]
**Type:** content
**Image:** yes
**Image Type:** content
**Title:** [Titel]
**Bullets:**
- [Bullet max. 7 Wörter]
- [Bullet]
**Speaker Notes:** [Notizen]
**Image Concept:** [Englisch, min. 20 Wörter, 9:16 Hochformat-Komposition, kein Text]

---

## Slide [N]
**Type:** visual
**Image:** yes
**Image Type:** visual
**Title:** [Kurzer Titel — max. 5 Wörter]
**Subtitle:** [Optionale Caption unter dem Bild]
**Speaker Notes:** [Notizen]
**Image Concept:** [Englisch, min. 30 Wörter — beschreibe das Erklärbild präzise als Diagramm / Infografik / Vergleich / Schema. Das Bild ersetzt Bullet-Text!]

---

## Slide [N]
**Type:** data
**Image:** no
**Image Type:** none
**Icons:** yes
**Icon 1:** [Englisch: Icon-Konzept]
**Icon 2:** [Englisch: Icon-Konzept]
**Title:** [Titel]
**Bullets:**
- [Datenpunkt]
**Speaker Notes:** [Notizen]
**Image Concept:** none
---SLIDE_STRUCTURE_END---
```

---

## Schritt 3 — Rolle: visual_designer v1

### Bilder generieren (nur Slides mit Image: yes):
```bash
cd [PROJEKT_PFAD]
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[vollständiger_prompt_min_25_wörter]" \
  --version 1 \
  --slide-type [image_type_aus_structure]
```

Prompt-Qualifier je Typ (immer anhängen):
- title/closing → "vertical portrait composition, [Stil-Qualifier], no text, no watermarks"
- section/visual → "wide horizontal composition, atmospheric, [Stil-Qualifier], no text, no watermarks"
- content → "vertical portrait format, professional, [Stil-Qualifier], no text, no watermarks"

Stil-Qualifier:
- dark-professional → "dark dramatic tones, cinematic lighting"
- light-modern → "bright clean modern, natural light"
- minimal → "high contrast minimalist, simple composition"
- bold-creative → "vibrant high energy, bold dramatic"

### Bildprinzipien (aus Leitfaden — beim Prompt schreiben beachten):

**Bild ≠ Text-Wiederholung:**
Das Bild erzeugt Stimmung oder Kontext — der Text liefert die Aussage. Wenn Bild und Text dasselbe sagen, ist eines davon überflüssig.

**Bild-Test (vor dem Prompt schreiben):**
Könnte man dieses Bild durch ein beliebiges anderes ersetzen, ohne dass sich die Aussage ändert? → Dann ist der Prompt zu generisch. Präziser formulieren: Was genau macht dieses Bild unverwechselbar für diesen Slide?

**Konsistenz über alle Slides:**
Alle Bilder müssen stilistisch zueinanderpassen — gleiche Farbtemperatur, Stimmung, Lichtstimmung. Kein Wechsel zwischen kalt/warm, dramatisch/flach, realistisch/abstrakt innerhalb derselben Präsentation.

**Vollflächige Bilder > Kasten-Bilder:**
Wenn das Bild die Folie tragen kann → `visual` oder `section` statt `content` (kein kleines Panel rechts).

### Icons generieren (Slides mit Icons: yes):
```bash
python scripts/generate_image.py \
  --slide [N] --version 1 --slide-type icon --icon-index [1|2|3] \
  --prompt "simple flat icon of [concept], bold single shape, white on dark background, minimal design, no text, no details, clean vector aesthetic, square format"
```

**Icon-Konsistenz:** Alle Icons einer Präsentation im gleichen Stil — entweder alle Flat, alle Outline oder alle Filled. Niemals mischen.

### image_manifest.md erstellen:
Halte in `workspace/image_manifest.md` fest: Slide, Typ, Prompt, Pfad, Status (generated/failed/skipped)

### PPTX v1 bauen:
```bash
python scripts/build_pptx.py --version 1 --style [STIL_AUS_STRUCTURE]
```
Bestätige: `output/presentations/presentation_v1.pptx` existiert.

---

## Schritt 4 — Rolle: critic v1 (2 Aufgaben)

### Aufgabe 1: Bilder prüfen

**A) Technische Dimensionsprüfung (PRIORITÄT 1):**
```python
python -c "
from PIL import Image; from pathlib import Path
for p in sorted(Path('output/images/v1').glob('*.png')):
    img = Image.open(p); print(f'{p.name}: {img.size[0]}x{img.size[1]}')
"
```
SOLL: title/closing=720×900 | content=640×900 | section=1280×720 | icon=256×256
IST ≠ SOLL → **Format Error: yes** → automatisch "Image Needs v2: yes"

**B) Inhaltliche Bildprüfung (1–5):**
- Format Fit: Hochformat vertikal komponiert? Querformat horizontal?
- Faithfulness: Passt Bildinhalt zum Slide-Thema? **Bild-Test: Wäre dieses Bild durch ein beliebiges anderes ersetzbar, ohne dass sich die Aussage ändert? → Score max. 2**
- Aesthetics: Professionelle Qualität, keine Artefakte? Konsistente Bildsprache mit den anderen Slides?
- Presentation Fit: Passt Farbton/Stil zur gewählten Palette?
- Complementarity: Wiederholt das Bild nur was der Text sagt? (Bild soll Stimmung/Kontext geben, nicht Text illustrieren) → wenn ja: Score max. 3

Score < 4 → "Image Needs v2: yes"

### Aufgabe 2: Slides prüfen — IMMER Textverbesserungen liefern

Für **jeden** Slide (nicht nur wenn Probleme da sind):

**Bewertung (1–5):**
- Content Quality: Titel + Bullets klar, prägnant, max. 6–7 Wörter pro Bullet? **Titel formuliert die Kernaussage (nicht nur ein Thema)?**
- Narrative Flow: Logischer Aufbau zum Vorgänger? Roter Faden erkennbar?
- Layout Balance: Textmenge passt zum Layout-Typ? Weißraum vorhanden?
- Slide Necessity: Notwendig oder zusammenlegbar? **Könnte dieser Slide weggelassen werden, ohne dass die Kernaussage verloren geht?**

**Textverbesserung (IMMER, für jeden Slide mit Bullets):**
Schreibe immer eine verbesserte Version von Titel und Bullets — auch wenn der Score 5/5 ist.
Ziel: maximale Klarheit, Kürze, Wirkung. Keine langen Halbsätze.
- Titel: max. 5 Wörter, Kernaussage
- Bullets: max. 6 Wörter, aktiv formuliert, konkret

Ausnahme: title/closing/section/visual Slides ohne Bullets → nur Titel prüfen, kein Improved Bullets.

### workspace/critique_v1.md erstellen:
```
# Critique Report — v1

## Übersicht
**Images Needing v2:** [Slide-Nummern]
**Slides with Content Changes:** [alle Slides mit Bullets]

## Slide 1
### Bild-Bewertung
**Expected Size:** 720×900px | **Actual Size:** [aus PIL]
**Format Error:** yes | no
**Format Fit:** [1-5] — [Begründung]
**Faithfulness:** [1-5] — [Begründung]
**Aesthetics:** [1-5] — [Begründung]
**Presentation Fit:** [1-5] — [Begründung]
**Image Needs v2:** yes | no
**Slide Type for v2:** [type]
**Refined Image Prompt v2:** [min. 30 Wörter wenn yes, sonst "none"]

### Slide-Bewertung
**Content Quality:** [1-5] — [Begründung]
**Narrative Flow:** [1-5] — [Begründung]
**Layout Balance:** [1-5] — [Begründung]
**Slide Necessity:** [1-5] — [Begründung]
**Improved Title:** [immer — auch wenn nur minimale Verbesserung]
**Improved Bullets:** [immer wenn Slide Bullets hat — jeder Bullet auf max. 6 Wörter]
```

---

## Schritt 5 — Rolle: visual_designer v2 (Feedback-Loop — BEIDE Korrekturen)

Lies `workspace/critique_v1.md` vollständig.

### A) slide_structure.md mit Textverbesserungen aktualisieren:
Für **jeden** Slide mit "Improved Title" oder "Improved Bullets" in critique_v1.md:
1. Titel ersetzen durch "Improved Title"
2. Bullets ersetzen durch "Improved Bullets"
3. Alle anderen Felder (Image Concept, Speaker Notes etc.) unverändert lassen
4. Nach jeder Änderung speichern

### B) Bilder regenerieren/kopieren:
```bash
# Image Needs v2: yes → neu generieren mit Critic-Prompt
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Image Prompt v2 aus critique_v1.md]" \
  --version 2 \
  --slide-type [Slide Type for v2 aus critique_v1.md]

# Image Needs v2: no → v1 übernehmen (Dateinamen enthalten Slug, daher Python)
python -c "
import shutil
from pathlib import Path
for f in Path('output/images/v1').glob('*_s[N:02d]_*.png'):
    shutil.copy2(f, Path('output/images/v2') / f.name)
"

# Icons immer aus v1 kopieren
python -c "
import shutil
from pathlib import Path
for f in Path('output/images/v1').glob('*_s[N:02d]_icon_*.png'):
    shutil.copy2(f, Path('output/images/v2') / f.name)
"
```

### C) PPTX v2 bauen:
slide_structure.md enthält jetzt die verbesserten Texte → v2 hat BEIDE Verbesserungen.
```bash
python scripts/build_pptx.py --version 2 --style [STIL_AUS_STRUCTURE]
```

---

## Schritt 6 — Rolle: critic v2

Gleiche Prüfung wie Schritt 4, jetzt auf v2-Ergebnissen.
Erstelle `workspace/critique_v2.md` (gleiches Format wie critique_v1.md).

Fokus: Was hat sich verbessert? Was ist noch nicht optimal?
- Bilder die in v2 neu generiert wurden: strengere Bewertung
- Texte die in v2 überarbeitet wurden: nochmals schärfen

Score-Schwelle für v3: Image Needs v3: yes wenn Score < 4.
Texte: Improved Title / Improved Bullets immer liefern.

---

## Schritt 7 — Rolle: visual_designer v3 (zweiter Feedback-Loop)

Gleiche Logik wie Schritt 5, jetzt auf Basis von `workspace/critique_v2.md`.

### A) slide_structure.md mit Textverbesserungen aus critique_v2.md aktualisieren

### B) Bilder regenerieren/kopieren (v2 → v3):
```bash
# Image Needs v3: yes → neu generieren
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Image Prompt v3 aus critique_v2.md]" \
  --version 3 \
  --slide-type [type]

# Image Needs v3: no → v2 übernehmen
python -c "
import shutil
from pathlib import Path
for f in Path('output/images/v2').glob('*.png'):
    shutil.copy2(f, Path('output/images/v3') / f.name)
"
```

### C) PPTX v3 bauen:
```bash
python scripts/build_pptx.py --version 3 --style [STIL_AUS_STRUCTURE]
```

---

## Schritt 8 — Rolle: critic final

Erstelle `workspace/final_report.md`:
```
# PresentationBanana — Final Report

**Recommended Version:** v3
**Overall Score v1:** [X.X / 5.0]
**Overall Score v2:** [X.X / 5.0]
**Overall Score v3:** [X.X / 5.0]
**Total Improvement:** [+X% gegenüber v1]

## Slide-by-Slide Comparison
| Slide | Type | Image? | v1 | v2 | v3 | Best |
|-------|------|--------|----|----|----|------|

## Content Changes v1→v2
- Slide [N]: "[alt]" → "[neu]"

## Content Changes v2→v3
- Slide [N]: "[alt]" → "[neu]"

## Image Improvements v1→v2
- Slide [N]: [was wurde korrigiert]

## Image Improvements v2→v3
- Slide [N]: [was wurde weiter verbessert]

## Summary
[3–5 Sätze: was hat der 3-stufige Loop insgesamt erreicht]
```

---

## Schritt 7 — Abschlussmeldung

```
✅ PresentationBanana fertig!

Ergebnisse:
- output/presentations/presentation_v1.pptx  (Score: [X.X])
- output/presentations/presentation_v2.pptx  (Score: [X.X]) ← Empfohlen

- [X] Slides mit verbessertem Bild in v2
- [X] Slides mit verbessertem Inhalt in v2
- Stil: [GEWÄHLTER_STIL]

Details: workspace/final_report.md
```
