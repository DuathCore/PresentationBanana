# PresentationBanana — Workflow-Beschreibung

**Autor:** Marek Teper
**Datum:** März 2026
**Typ:** Technisches Konzeptpaper

---

## Was ist PresentationBanana?

PresentationBanana ist ein KI-gestützter Workflow zur vollautomatischen Erstellung professioneller PowerPoint-Präsentationen. Er kombiniert Inhaltsanalyse, KI-Bildgenerierung und einen iterativen Critic-Visualizer-Loop zu einem geschlossenen Produktionssystem — ohne manuellen Eingriff zwischen Eingabe und Endprodukt.

Das System arbeitet als sequenzieller Solo-Workflow: Claude Code übernimmt nacheinander alle Rollen selbst — Stratege, Bildgestalter, Kritiker, Korrektor.

---

## Architektur: Die vier Rollen

### 1. Content Strategist
Analysiert den Input (Text, PDF oder PPTX) und erstellt die `slide_structure.md` — eine strukturierte Blaupause mit Slide-Typ, Titel, Bullets, Speaker Notes und Bildkonzept für jeden Slide. Die Anzahl der Slides und der visuelle Stil werden automatisch passend zum Thema gewählt, können aber auch manuell vorgegeben werden.

### 2. Visual Designer
Generiert alle Bilder via Google Imagen 4 (Fallback: Gemini 2.5 Flash Image) und baut daraus eine PPTX-Datei mit `python-pptx`. Jeder Slide-Typ hat ein eigenes Layout und eine eigene Bildgröße:
- **title / closing:** 720×900 px (9:16 Hochformat, Bildpanel links/rechts)
- **content:** 640×900 px (9:16 Hochformat, Textpanel + Bildpanel)
- **section:** 1280×720 px (16:9 Querformat, Vollbild-Hintergrund)
- **icon:** 256×256 px (1:1 Quadrat, für Daten-Slides)

### 3. Critic
Bewertet jedes Bild (Format, Bildinhalt, Qualität, Stilfit) und jeden Slide-Text (Klarheit, narrativer Fluss, Kürze) auf einer Skala von 1–5. Der Critic liefert immer verbesserte Titel und Bullets — nicht nur bei Problemen. Bilder mit Score < 4 werden zur Neugenerierung markiert.

### 4. Visual Designer v2/v3 (Feedback-Loop)
Liest die Kritik und wendet alle Verbesserungen an: überarbeitete Texte in die `slide_structure.md`, flagged Bilder werden mit präzisierten Prompts neu generiert, unveränderte Bilder werden übernommen. Dann wird die PPTX neu gebaut.

---

## Der Drei-Stufen-Loop

PresentationBanana durchläuft drei vollständige Iterationen:

```
v1: Erstgenerierung
  ↓ Critic → critique_v1.md
v2: Korrekturen (Bilder + Texte)
  ↓ Critic → critique_v2.md
v3: Feinschliff (zweite Runde)
  ↓ Final Report
```

Jede Stufe verbessert sowohl die Bilder als auch die Slide-Texte. Der finale Bericht vergleicht alle drei Versionen mit Scores und zeigt den Gesamtfortschritt.

---

## Technischer Stack

| Komponente | Technologie |
|---|---|
| Präsentation | python-pptx |
| Bildgenerierung | Google Imagen 4 / Gemini 2.5 Flash Image |
| Dateinamen | Slug-basiert aus Thema (z.B. `presentation-banana_s01_title.png`) |
| Stil-Optionen | dark-professional, light-modern, minimal, bold-creative |
| Einstieg | `/presentation-banana` in Claude Code |
| Konfiguration | `.claude/settings.local.json` (API-Key, Berechtigungen) |

---

## Dateisystem-Struktur

```
06_PresentationBanana/
├── input/                    ← Eingabe-Dokumente
├── workspace/
│   ├── slide_structure.md    ← Folienpläne (wird in jedem Loop aktualisiert)
│   ├── image_manifest.md     ← Bildübersicht
│   ├── critique_v1.md        ← Critic-Bericht nach v1
│   ├── critique_v2.md        ← Critic-Bericht nach v2
│   └── final_report.md       ← Gesamtvergleich v1/v2/v3
├── output/
│   ├── images/v1/            ← Bilder Iteration 1
│   ├── images/v2/            ← Bilder Iteration 2
│   ├── images/v3/            ← Bilder Iteration 3
│   └── presentations/        ← PPTX v1, v2, v3
└── scripts/
    ├── generate_image.py     ← Imagen-Wrapper
    └── build_pptx.py         ← PPTX-Builder
```

---

## Kernprinzip: Der Critic-Visualizer-Loop

Das entscheidende Designprinzip ist der geschlossene Feedback-Loop: Der Critic bewertet nicht nur, sondern formuliert konkrete Verbesserungen — präzisere Bild-Prompts, kürzere Titel, schärfere Bullets. Der Visual Designer der nächsten Iteration wendet diese Verbesserungen mechanisch an. Dieses Prinzip ist direkt übertragen vom PaperBanana-Ansatz (Claude Agent Teams) auf einen sequenziellen Solo-Workflow ohne externe Abhängigkeiten.

Nach drei Iterationen hat sich gezeigt: Die kritischsten Verbesserungen passieren in v2 (falsche Bilder, zu lange Titel). v3 liefert Feinschliff (Farbton-Kohärenz, Bullet-Prägnanz). Der Gesamtfortschritt von v1 zu v3 beträgt typisch +25–40% auf der 5-Punkte-Skala.
