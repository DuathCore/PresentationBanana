---
name: image-banana
description: >
  Generiert KI-Bilder mit iterativem Critic-Visualizer-Loop via Gemini Imagen.
  Konzeptanalyse → Bildgenerierung v1 → Critic → Verbesserung v2 → Critic → v3 → Finalbericht.
  Trigger: wenn der User Bilder, Grafiken oder eine Bilderserie generieren möchte,
  ohne eine Präsentation zu erstellen.
---

# ImageBanana

Du führst alle Schritte selbst durch — sequenziell, ohne Teammates.
Projektverzeichnis: Das aktuelle Arbeitsverzeichnis (muss `scripts/generate_image.py` enthalten).

---

## Schritt 1 — Konfiguration erfassen

### 1.1 Input
Falls nicht angegeben, frage: "Was für Bilder soll ich generieren?"

Mögliche Inputs:
- Einzelnes Bildkonzept (Freitext)
- Liste von Bildkonzepten (nummeriert oder als Bullets)
- Thema für eine zusammenhängende Bilderserie (z.B. "5 Bilder zum Thema Nachhaltigkeit")
- PDF/Text als Inspirationsquelle

### 1.2 Stil-Feeling
Frage: "Welchen visuellen Stil sollen die Bilder haben?"

Vorschläge zeigen:
```
1. cinematic       → Filmisch, dramatisches Licht, tiefe Farben
2. editorial       → Magazin-Look, clean, modern, natürliches Licht
3. minimalist      → Reduiert, viel Weißraum, klare Formen
4. abstract        → Experimentell, Texturen, unkonventionell
5. documentary     → Authentisch, reportagehaft, ehrlich
6. eigene Eingabe  → Freie Stil-Beschreibung
```

### 1.3 Format
Frage: "Welches Format sollen die Bilder haben?"

```
1. 16:9 Querformat    → 1280×720px (Widescreen, Hintergründe, Banner)
2. 9:16 Hochformat    → 720×900px  (Porträts, Social Stories, Poster)
3. 1:1 Quadrat        → 512×512px  (Social Media, Icons, Profilbilder)
4. Custom Größe       → z.B. 3440×1440, 1920×1080, 2560×1440 (beliebig)
5. Gemischt           → Pro Bild individuell festlegen
```

Bei Custom Größe nach **Breite × Höhe in Pixeln** fragen.
Das nächste Gemini-Aspect-Ratio wird automatisch gewählt (1:1, 3:4, 4:3, 9:16, 16:9).

### 1.4 Serie
Falls mehrere Bilder: "Sollen die Bilder eine zusammenhängende Serie sein?"
- **Ja** → Konsistenz-Regeln aktiv (gleiche Farbtemperatur, Stimmung, Lichtstimmung)
- **Nein** → Jedes Bild unabhängig

### 1.5 Anzahl
Falls nicht aus Input ersichtlich: "Wie viele Bilder?" (Default: aus Konzeptliste)

Kurze Zusammenfassung zeigen + Bestätigung abwarten.

---

## Schritt 2 — Rolle: concept_strategist

Analysiere den Input und erstelle `workspace/image_concepts.md`.

### Konzept-Erstellung:

Für jedes Bild ein detailliertes englisches Konzept erstellen:
- Min. 25 Wörter
- Lichtstimmung beschreiben (warm golden light / cool blue tones / dramatic shadows)
- Perspektive beschreiben (wide angle / close-up / aerial / eye level)
- Stil beschreiben (cinematic / documentary / editorial / minimalist)
- Kein Text, kein Logo, kein Wasserzeichen
- Bei Serien: konsistente Stichworte für Farbton und Stimmung in allen Konzepten

### Format workspace/image_concepts.md:
```
---IMAGE_CONCEPTS_START---
# Image Concepts

**Theme:** [Übergeordnetes Thema]
**Style:** [Gewählter Stil + Qualifiers]
**Series:** yes | no
**Total Images:** [Anzahl]

---

## Image 1
**Format:** 16:9 | 9:16 | 1:1 | custom
**Size:** 1280x720 | 720x900 | 512x512 | [BREITExHOEHE]
**Concept:** [Englisch, min. 25 Wörter, vollständiges Bildkonzept]

---

## Image 2
**Format:** [...]
**Size:** [...]
**Concept:** [...]

---IMAGE_CONCEPTS_END---
```

---

## Schritt 3 — Rolle: image_generator v1

### Bilder generieren:

Für jedes Bild aus image_concepts.md:

```bash
# Preset-Formate:
python scripts/generate_image.py \
  --slide [BILD_NUMMER] \
  --prompt "[concept_aus_image_concepts_md]" \
  --version 1 \
  --slide-type [FORMAT_MAPPING] \
  --name [THEMA_SLUG]

# Custom-Größe:
python scripts/generate_image.py \
  --slide [BILD_NUMMER] \
  --prompt "[concept_aus_image_concepts_md]" \
  --version 1 \
  --width [BREITE] --height [HOEHE] \
  --name [THEMA_SLUG]
```

**`--name` IMMER setzen!** Leite einen kurzen englischen Slug vom Thema ab (z.B. "sustainability-series", "brand-icons", "nature-wallpapers").

**Format-Mapping für --slide-type (nur bei Preset-Formaten):**
- 16:9 → `section`
- 9:16 → `content`
- 1:1 → `icon`

Prüfe JSON-Antwort auf `"ok": true`.
Bei Fehler: Prompt vereinfachen und erneut versuchen.

### image_manifest.md erstellen:
Halte in `workspace/image_manifest.md` fest:
```
# Image Manifest — v1

## Image 1
**Format:** 16:9
**Prompt Used:** [vollständiger Prompt]
**Output Size:** 1280×720px
**Status:** generated | failed
**Path:** output/images/v1/[filename]

## Image 2
...
```

---

## Schritt 4 — Rolle: image_critic v1

### Technische Prüfung (PRIORITÄT 1):
```python
python -c "
from PIL import Image; from pathlib import Path
for p in sorted(Path('output/images/v1').glob('*.png')):
    img = Image.open(p); print(f'{p.name}: {img.size[0]}x{img.size[1]}')
"
```

SOLL-Abmessungen: 16:9→1280×720 | 9:16→720×900 | 1:1→512×512 | Custom→wie in image_concepts.md angegeben
IST ≠ SOLL → Format Error → automatisch "Needs v2: yes"

### Inhaltliche Bewertung (1–5 pro Kriterium):

- **Composition:** Bildaufbau, visuelle Schwerpunkte, Linienführung, Nutzung des Formats
- **Faithfulness:** Passt der Bildinhalt zum gewünschten Konzept? Sind alle beschriebenen Elemente vorhanden?
- **Aesthetics:** Professionelle Qualität? Keine Artefakte, verzerrte Proportionen oder unnatürliche Elemente?
- **Style Consistency:** (nur bei Serien) Passt das Bild stilistisch zum Rest? Gleiche Farbtemperatur, Stimmung?
- **Mood/Impact:** Erzeugt das Bild die gewünschte emotionale Wirkung? Ist es einprägsam?

Score < 4 in irgendeinem Kriterium → "Needs v2: yes"

### workspace/image_critique_v1.md erstellen:
```
# Image Critique — v1

## Übersicht
**Images Needing v2:** [Bild-Nummern]
**Average Score:** [X.X / 5.0]

---

## Image 1
**Expected Size:** 1280×720px | **Actual Size:** [aus PIL]
**Format Error:** yes | no
**Composition:** [1-5] — [Begründung]
**Faithfulness:** [1-5] — [Begründung]
**Aesthetics:** [1-5] — [Begründung]
**Style Consistency:** [1-5] — [Begründung, oder "N/A" wenn keine Serie]
**Mood/Impact:** [1-5] — [Begründung]
**Needs v2:** yes | no
**Refined Prompt v2:** [min. 30 Wörter wenn yes — konkret was verbessert wird. Sonst "none"]

---

## Image 2
...
```

---

## Schritt 5 — Rolle: image_generator v2 (Feedback-Loop)

Lies `workspace/image_critique_v1.md` vollständig.

### Bilder regenerieren/kopieren:
```bash
# Needs v2: yes → neu generieren mit Critic-Prompt
# Preset-Format:
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Prompt v2 aus image_critique_v1.md]" \
  --version 2 \
  --slide-type [FORMAT_MAPPING] \
  --name [THEMA_SLUG]

# Custom-Größe:
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Prompt v2 aus image_critique_v1.md]" \
  --version 2 \
  --width [BREITE] --height [HOEHE] \
  --name [THEMA_SLUG]

# Needs v2: no → v1 übernehmen
python -c "
import shutil
from pathlib import Path
for f in Path('output/images/v1').glob('*_s[N:02d]_*.png'):
    shutil.copy2(f, Path('output/images/v2') / f.name)
"
```

### image_manifest.md ergänzen:
```
---V2_CHANGES_START---
# Changes Applied in v2

## Regenerated Images
- Image [N]: [Grund aus Critique] — neuer Prompt

## Carried Over (unchanged)
- Image [N]: v1 → v2
---V2_CHANGES_END---
```

---

## Schritt 6 — Rolle: image_critic v2

Gleiche Prüfung wie Schritt 4, jetzt auf v2-Ergebnissen.
Erstelle `workspace/image_critique_v2.md` (gleiches Format).

Fokus:
- Haben sich die regenerierten Bilder verbessert?
- Strengere Bewertung für v2-Bilder
- Score < 4 → "Needs v3: yes"

---

## Schritt 7 — Rolle: image_generator v3 (zweiter Feedback-Loop)

Gleiche Logik wie Schritt 5, auf Basis von `workspace/image_critique_v2.md`.

```bash
# Needs v3: yes → neu generieren
# Preset-Format:
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Prompt v3 aus image_critique_v2.md]" \
  --version 3 \
  --slide-type [FORMAT_MAPPING] \
  --name [THEMA_SLUG]

# Custom-Größe:
python scripts/generate_image.py \
  --slide [N] \
  --prompt "[Refined Prompt v3 aus image_critique_v2.md]" \
  --version 3 \
  --width [BREITE] --height [HOEHE] \
  --name [THEMA_SLUG]

# Needs v3: no → v2 übernehmen
python -c "
import shutil
from pathlib import Path
for f in Path('output/images/v2').glob('*_s[N:02d]_*.png'):
    shutil.copy2(f, Path('output/images/v3') / f.name)
"
```

---

## Schritt 8 — Final Report

Erstelle `workspace/image_final_report.md`:
```
# ImageBanana — Final Report

**Recommended Version:** v3
**Average Score v1:** [X.X / 5.0]
**Average Score v2:** [X.X / 5.0]
**Average Score v3:** [X.X / 5.0]
**Total Improvement:** [+X% gegenüber v1]

## Image-by-Image Comparison

| Image | Format | v1 Score | v2 Score | v3 Score | Best |
|-------|--------|----------|----------|----------|------|
| 1     | 16:9   | 3.4      | 4.2      | 4.6      | v3   |
| 2     | 9:16   | 4.0      | 4.0      | 4.0      | —    |

## Improvements v1→v2
- Image [N]: [was wurde verbessert]

## Improvements v2→v3
- Image [N]: [was wurde weiter verbessert]

## Summary
[3–5 Sätze: Gesamtverbesserung durch den Critic-Visualizer-Loop]
```

---

## Abschlussmeldung

```
✅ ImageBanana fertig!

Ergebnisse:
- output/images/v1/  (Score: [X.X])
- output/images/v2/  (Score: [X.X])
- output/images/v3/  (Score: [X.X]) ← Empfohlen

- [X] von [Y] Bildern in v2 verbessert
- [X] von [Y] Bildern in v3 weiter verfeinert
- Stil: [GEWÄHLTER_STIL]

Details: workspace/image_final_report.md
```
