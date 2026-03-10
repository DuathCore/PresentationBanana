# PresentationBanana — CLAUDE.md

Diese Datei gibt Claude Code (und dem Claude Skill) alle nötigen Informationen
zum automatischen Erstellen von KI-generierten PowerPoint-Präsentationen.

---

## Projektstruktur

```
06_PresentationBanana/
├── input/          ← Thema (topic.md), PDF oder PPTX ablegen
├── output/
│   ├── images/v1/  ← Bilder Iteration 1
│   ├── images/v2/  ← Bilder Iteration 2 (verfeinert)
│   └── presentations/  ← presentation_v1.pptx, presentation_v2.pptx
├── workspace/      ← Temporäre Agenten-Kommunikation (nicht löschen!)
├── scripts/        ← Python-Skripte (nicht ändern)
└── prompts/        ← Spawn-Prompt für Claude Code Agent Teams
```

---

## Style-Optionen

Bei jedem neuen Projekt MUSS der Stil definiert werden.
Falls der Nutzer keinen Stil angibt, FRAGE nach einem der folgenden:

| Style-Name         | Beschreibung                          | Typische Anwendung            |
|--------------------|---------------------------------------|-------------------------------|
| `dark-professional`| Navy-Hintergrund, Gold-Akzente        | Unternehmens-, Investoren-Pitch |
| `light-modern`     | Weißer Hintergrund, Teal-Akzente      | Produkt, Startup, Tech        |
| `minimal`          | Reinweiß, schwarz, grau               | Design, Architektur, Kreativ  |
| `bold-creative`    | Schwarz, Orange-Rot-Akzente           | Marketing, Events, Agentur    |

---

## Slide-Typen

| Type       | Layout                                  |
|------------|-----------------------------------------|
| `title`    | Bild rechts, Titel + Subtitle links     |
| `content`  | Text + Bullets links, Bild rechts       |
| `section`  | Zentrierter Text, kein Bild             |
| `closing`  | Bild links, Titel + CTA rechts          |

---

## Technische Voraussetzungen

```bash
pip install python-pptx google-generativeai pillow pymupdf
```

**GOOGLE_API_KEY** ist in `.claude/settings.local.json` einzutragen (dort `HIER-DEINEN-KEY-EINTRAGEN` ersetzen).

**Modell:** Alle Teammates laufen auf `claude-sonnet-4-6` — in `.claude/settings.local.json` als Default hinterlegt.

### Agent Teams Setup (PFLICHT für den vollständigen Workflow)

**`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** ist bereits in `.claude/settings.local.json` gesetzt.

**Claude Code MUSS innerhalb einer tmux-Session gestartet werden:**
```bash
# 1. Neue tmux-Session starten
tmux new-session -s presentation-banana

# 2. Claude Code im Projektordner starten
cd /path/to/PresentationBanana
claude

# Optional: Ohne Permission-Prompts (vollständig autonom)
claude --dangerously-skip-permissions
```

**Ohne tmux** können keine Teammates gespawnt werden — Claude arbeitet dann solo (kein Agent Team).

---

## Workflow-Übersicht

```
1. content_strategist   → workspace/slide_structure.md
2. visual_designer (v1) → output/images/v1/ + presentation_v1.pptx
3. critic               → workspace/critique_v1.md
4. visual_designer (v2) → output/images/v2/ + presentation_v2.pptx
5. critic (final)       → workspace/final_report.md
```

---

## Wichtige Regeln für Claude

1. **Style immer abfragen** wenn nicht explizit angegeben — niemals raten
2. **Image Concepts immer auf Englisch** für Gemini Imagen
3. **Kein Text in Bildern** — immer explizit im Prompt verbieten
4. **workspace/** Dateien zwischen Agenten nicht löschen
5. **JSON-Output** der Skripte auf `"ok": true` prüfen vor nächstem Schritt
6. Bei `"ok": false` → Fehler ausgeben und User fragen wie vorzugehen ist
7. **Bilder generieren dauert** ~5–15 Sekunden pro Bild — normal und kein Fehler

---

## Kosten-Hinweise

- Gemini Imagen 3: ca. $0.04 pro Bild (16:9)
- 10 Slides × 2 Iterationen = ~$0.80 Bildkosten
- Claude Agent Teams: 3 Teammates ≈ 4× Token-Kosten vs. normaler Betrieb
- Gesamtkosten typische Präsentation (10 Slides): $2–5

---

## Fehler-Handling

| Fehler                          | Lösung                                    |
|---------------------------------|-------------------------------------------|
| `GOOGLE_API_KEY not set`        | `export GOOGLE_API_KEY=...` ausführen     |
| `No image returned by API`      | Prompt vereinfachen, weniger spezifisch   |
| `slide_structure.md not found`  | content_strategist erneut laufen lassen   |
| Bild fehlt im PPTX              | Platzhalter wird automatisch eingefügt    |
| `python-pptx not installed`     | `pip install python-pptx` ausführen       |
