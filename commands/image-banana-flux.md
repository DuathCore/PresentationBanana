---
name: image-banana-flux
description: >
  Generiert KI-Bilder mit Flux.1 Dev über einen Remote-GPU-Server.
  Gleicher Critic-Visualizer-Loop wie image-banana, aber mit Flux statt Imagen.
  Keine Content-Filter — volle kreative Freiheit.
  Trigger: wenn der User Bilder mit Flux generieren möchte.
---

# ImageBanana Flux

Du führst alle Schritte selbst durch — sequenziell, ohne Teammates.
Projektverzeichnis: Das aktuelle Arbeitsverzeichnis (muss `scripts/generate_image_flux.py` enthalten).

**Backend:** Flux.1 Dev auf Remote-GPU-Server (kein Content-Filter).
**Script:** `scripts/generate_image_flux.py` (statt `generate_image.py`)

---

## Schritt 1 — Konfiguration erfassen

### 1.1 Input
Falls nicht angegeben, frage: "Was für Bilder soll ich generieren?"

Mögliche Inputs:
- Einzelnes Bildkonzept (Freitext)
- Liste von Bildkonzepten (nummeriert oder als Bullets)
- Thema für eine zusammenhängende Bilderserie
- PDF/Text als Inspirationsquelle

### 1.2 Stil-Feeling
Frage: "Welchen visuellen Stil sollen die Bilder haben?"

Vorschläge zeigen:
```
1. cinematic       → Filmisch, dramatisches Licht, tiefe Farben
2. editorial       → Magazin-Look, clean, modern, natürliches Licht
3. minimalist      → Reduziert, viel Weißraum, klare Formen
4. abstract        → Experimentell, Texturen, unkonventionell
5. documentary     → Authentisch, reportagehaft, ehrlich
6. photorealistic  → Fotorealistisch, nicht von echtem Foto unterscheidbar
7. eigene Eingabe  → Freie Stil-Beschreibung
```

### 1.3 Format
Frage: "Welches Format sollen die Bilder haben?"

```
1. 16:9 Querformat    → 1280×720px
2. 9:16 Hochformat    → 720×1280px
3. 1:1 Quadrat        → 512×512px
4. Surface Pro 7      → 2736×1824px
5. Full HD            → 1920×1080px
6. 2K                 → 2560×1440px
7. Ultrawide          → 3440×1440px
8. Custom Größe       → beliebig (muss durch 16 teilbar sein!)
9. Gemischt           → Pro Bild individuell
```

**WICHTIG:** Flux braucht Dimensionen die durch 16 teilbar sind. Bei Custom automatisch runden.

### 1.4 Serie
Falls mehrere Bilder: "Sollen die Bilder eine zusammenhängende Serie sein?"
- **Ja** → Konsistenz-Regeln aktiv
- **Nein** → Jedes Bild unabhängig

### 1.5 Anzahl
Falls nicht aus Input ersichtlich: "Wie viele Bilder?"

### 1.6 Server-Check
Vor dem Start prüfen ob der Flux-Server erreichbar ist:
```bash
python3 scripts/generate_image_flux.py --slide 0 --prompt "test" --version 0 --name test 2>&1
```
Falls Server nicht erreichbar → User informieren und IP/Port erfragen.

Kurze Zusammenfassung zeigen + Bestätigung abwarten.

---

## Schritt 2 — Rolle: concept_strategist

Analysiere den Input und erstelle `workspace/image_concepts.md`.

### Konzept-Erstellung (Flux-optimiert):

Für jedes Bild ein detailliertes englisches Konzept erstellen:
- Min. 30 Wörter, max. 200 Wörter (Flux Sweet Spot)
- **Wichtigstes zuerst** — Flux gewichtet den Anfang stärker
- Lichtstimmung beschreiben
- Perspektive beschreiben
- Stil beschreiben
- Materialien und Texturen explizit benennen
- Bei Serien: konsistente Stichworte für Farbton und Stimmung

### Negative Prompt:
Für jedes Bild auch einen Negative Prompt definieren:
- Standard: "text, watermark, logo, blurry, low quality, deformed hands, extra fingers"
- Pro Bild ergänzen falls nötig

### Format workspace/image_concepts.md:
```
---IMAGE_CONCEPTS_START---
# Image Concepts (Flux)

**Theme:** [Übergeordnetes Thema]
**Style:** [Gewählter Stil + Qualifiers]
**Series:** yes | no
**Total Images:** [Anzahl]
**Backend:** Flux.1 Dev

---

## Image 1
**Format:** [Preset oder Custom]
**Size:** [BREITExHÖHE]
**Concept:** [Englisch, 30-200 Wörter, Wichtigstes zuerst]
**Negative:** [Negative Prompt]

---
---IMAGE_CONCEPTS_END---
```

---

## Schritt 3 — Rolle: image_generator v1

### Bilder generieren:

Für jedes Bild aus image_concepts.md:

```bash
python3 scripts/generate_image_flux.py \
  --slide [BILD_NUMMER] \
  --prompt "[concept]" \
  --negative "[negative_prompt]" \
  --version 1 \
  --width [BREITE] --height [HÖHE] \
  --name [THEMA_SLUG]
```

Oder mit Preset:
```bash
python3 scripts/generate_image_flux.py \
  --slide [BILD_NUMMER] \
  --prompt "[concept]" \
  --negative "[negative_prompt]" \
  --version 1 \
  --preset surface \
  --name [THEMA_SLUG]
```

**`--name` IMMER setzen!**

Prüfe JSON-Antwort auf `"ok": true`.
Bei Fehler: Prompt vereinfachen und erneut versuchen.

---

## Schritt 4 — Rolle: image_critic v1 + User-Kritik

### Technische Prüfung:
```python
python3 -c "
from PIL import Image; from pathlib import Path
for p in sorted(Path('output/images').glob('*_v1.png')):
    img = Image.open(p); print(f'{p.name}: {img.size[0]}x{img.size[1]}')
"
```

### AI Critic Bewertung (1–5 pro Kriterium):

- **Composition:** Bildaufbau, visuelle Schwerpunkte, Nutzung des Formats
- **Faithfulness:** Passt der Bildinhalt zum Konzept? Alle Elemente vorhanden?
- **Aesthetics:** Professionelle Qualität? Artefakte? Proportionen?
- **Style Consistency:** (nur bei Serien) Stilistisch konsistent?
- **Mood/Impact:** Emotionale Wirkung, Einprägsamkeit
- **Hands/Details:** Hände korrekt? Finger richtig? Details sauber?

Score < 4 in irgendeinem Kriterium → "Needs v2: yes"

### User-Kritik einholen:
**WICHTIG: Nach JEDER Critic-Runde den User fragen:**
"Deine Kritik?"

User-Feedback hat VORRANG vor AI-Critic. Wenn der User etwas anders will,
wird das in den v2/v3 Prompt eingebaut — auch wenn der AI-Critic es gut fand.

### workspace/image_critique_v1.md erstellen:
```
# Image Critique — v1 (Flux)

## AI Critic
[Bewertung wie oben]

## User Kritik
[Was der User gesagt hat]

## Refined Prompt v2
[Kombiniert AI + User Feedback, min. 30 Wörter]
**Negative v2:** [Angepasster Negative Prompt]
```

---

## Schritt 5 — Rolle: image_generator v2

Lies `workspace/image_critique_v1.md` und generiere v2 mit dem verbesserten Prompt.

```bash
python3 scripts/generate_image_flux.py \
  --slide [N] \
  --prompt "[Refined Prompt v2]" \
  --negative "[Negative v2]" \
  --version 2 \
  --width [BREITE] --height [HÖHE] \
  --name [THEMA_SLUG]
```

---

## Schritt 6 — Rolle: image_critic v2 + User-Kritik

Gleiche Prüfung wie Schritt 4, auf v2-Ergebnissen.
**User-Kritik wieder einholen!**
Erstelle `workspace/image_critique_v2.md`.

---

## Schritt 7 — Rolle: image_generator v3

Gleiche Logik wie Schritt 5, auf Basis von v2-Critique.

---

## Schritt 8 — Final Report

Erstelle `workspace/image_final_report.md`:
```
# ImageBanana Flux — Final Report

**Backend:** Flux.1 Dev (Remote GPU)
**Recommended Version:** v3
**Average Score v1:** [X.X / 5.0]
**Average Score v2:** [X.X / 5.0]
**Average Score v3:** [X.X / 5.0]

## Image-by-Image Comparison

| Image | Format | v1 Score | v2 Score | v3 Score | Best |
|-------|--------|----------|----------|----------|------|
| 1     | ...    | ...      | ...      | ...      | ...  |

## User Feedback Integration
[Welches User-Feedback wurde eingebaut und wie]

## Summary
[3–5 Sätze]
```

---

## Flux-spezifische Prompting-Regeln

1. **Wichtigstes zuerst** — Flux gewichtet den Prompt-Anfang stärker
2. **Natürliche Sprache** — Keine Keyword-Listen, sondern Sätze
3. **Negative Prompts nutzen** — Über `--negative` Flag
4. **Max 200 Wörter** — Darüber vergisst Flux Details
5. **Stil-Keywords am Ende** — "cinematic lighting, 8k, photorealistic, masterpiece"
6. **Hände explizit beschreiben** — "correct five fingers on each hand, anatomically correct hands"
7. **Keine Content-Beschränkungen** — Flux hat keinen Content-Filter

---

## Abschlussmeldung

```
✅ ImageBanana Flux fertig!

Ergebnisse in output/images/
- v1 Bilder (Score: [X.X])
- v2 Bilder (Score: [X.X])
- v3 Bilder (Score: [X.X]) ← Empfohlen

Backend: Flux.1 Dev
User-Feedback: [X] Runden eingebaut

Details: workspace/image_final_report.md
```
