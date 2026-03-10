# PresentationBanana

**AI-powered PowerPoint presentations and standalone images with Gemini Imagen + Claude Code.**

Takes a topic, PDF, or existing PPTX as input and generates a polished presentation with AI-generated images — fully automated through a Critic-Visualizer feedback loop.

## How It Works

### `/presentation-banana` — Full Presentation Workflow

```
Content Strategist  →  slide_structure.md
        ↓
Visual Designer v1  →  AI images + presentation_v1.pptx
        ↓
Critic              →  scores each slide & image, writes improvements
        ↓
Visual Designer v2  →  refined images + presentation_v2.pptx
        ↓
Final Report        →  v1 vs v2 comparison
```

### `/image-banana` — Standalone Image Generation

```
Concept Strategist  →  image_concepts.md
        ↓
Image Generator v1  →  output/images/v1/
        ↓
Image Critic v1     →  scores & improvement prompts
        ↓
Image Generator v2  →  output/images/v2/ (refined)
        ↓
Image Critic v2     →  final scoring
        ↓
Image Generator v3  →  output/images/v3/ (polished)
```

Three iterations with critic feedback — typical improvement: +25–40% on the 5-point quality scale.

## Features

- Iterative Critic-Visualizer feedback loop (v1 → Critic → v2 → v3)
- Preset formats: 16:9, 9:16, 1:1
- Custom sizes: any resolution (e.g. 3440x1440 ultrawide, 1920x1080 Full HD)
- Series mode: consistent style across multiple images
- Fallback: Imagen 4 → Gemini 2.5 Flash (auto)
- Agent Teams: parallel teammates for faster execution (requires tmux)

## Example

[View example presentation (PDF)](examples/rome-wasnt-built-in-a-day.pdf)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API key

Copy the example and add your [Google AI Studio](https://aistudio.google.com/apikey) key:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder with your actual key:

```
GOOGLE_API_KEY=your-google-api-key-here
```

### 3. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 4. Copy Claude Code settings

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

## Usage

### Presentations

```bash
cd PresentationBanana
claude
```

Then type `/presentation-banana`. Claude asks for your topic, style, and slide count — then runs the full workflow.

### Standalone Images

Type `/image-banana`. Same Critic-Visualizer loop, but focused purely on image quality. Supports:

- Single images or batches
- Consistent series (same color temperature, mood, lighting)
- Preset formats (16:9, 9:16, 1:1) or any custom size

### Input Options

Place your input in the `input/` folder:

- **`input/topic.md`** — Describe your topic (template included)
- **`input/document.pdf`** — Extract content from a PDF
- **`input/existing.pptx`** — Redesign an existing presentation

### Styles (Presentations)

| Style | Look | Best for |
|-------|------|----------|
| `dark-professional` | Navy + Gold | Corporate, investor pitch |
| `light-modern` | White + Teal | Product, startup, tech |
| `minimal` | White + Black | Design, architecture |
| `bold-creative` | Black + Orange-Red | Marketing, events |

### Agent Teams (full autonomy)

For the multi-agent workflow with parallel teammates, start Claude Code inside a tmux session:

```bash
tmux new-session -s presentation-banana
cd PresentationBanana
claude
```

Without tmux, Claude runs the workflow solo (still works, just sequential).

## Manual Script Usage

### Generate images

```bash
# Slide preset (for presentations)
python scripts/generate_image.py \
  --slide 3 \
  --prompt "modern boardroom meeting, warm lighting, professional" \
  --slide-type content --version 1

# Custom size (e.g. ultrawide wallpaper)
python scripts/generate_image.py \
  --slide 1 \
  --prompt "panoramic mountain landscape at sunset" \
  --width 3440 --height 1440 \
  --name mountain-wallpaper

# Custom size with explicit aspect ratio
python scripts/generate_image.py \
  --slide 1 \
  --prompt "abstract geometric pattern" \
  --width 1920 --height 1080 \
  --aspect-ratio 16:9 --name banner
```

**Options:**

| Flag | Description |
|------|-------------|
| `--slide` | Image number (required) |
| `--prompt` | Image description in English (required) |
| `--slide-type` | Preset: `content`, `title`, `closing`, `section`, `visual`, `icon` |
| `--width` / `--height` | Custom pixel dimensions (overrides `--slide-type`) |
| `--aspect-ratio` | Override auto-detected Gemini ratio (`1:1`, `3:4`, `4:3`, `9:16`, `16:9`) |
| `--name` | Filename prefix (e.g. `wallpaper`, `brand-icons`) |
| `--version` | Output iteration folder: v1, v2, v3 (default: 1) |

### Build presentation

```bash
python scripts/build_pptx.py --version 1 --style light-modern
```

## Project Structure

```
PresentationBanana/
├── commands/           ← Skill definitions (image-banana, presentation-banana)
├── examples/           ← Example output (PDF preview)
├── input/              ← Your topic, PDF, or PPTX
├── output/
│   ├── images/v1–v3/   ← Generated images per iteration
│   └── presentations/  ← Final PPTX files
├── scripts/            ← Python scripts (generate_image.py, build_pptx.py)
├── workspace/          ← Temp files between agents (auto-generated)
└── prompts/            ← Agent team spawn prompts
```

## Cost Estimates

| Item | Cost |
|------|------|
| Gemini Imagen (per image) | ~$0.04 |
| 10 slides x 2 iterations | ~$0.80 |
| Image-only (5 images x 3 iterations) | ~$0.60 |
| Claude tokens (agent team) | ~$1–3 |
| **Total (10-slide presentation)** | **$2–5** |

## Tech Stack

- **Presentation builder:** [python-pptx](https://python-pptx.readthedocs.io/)
- **Image generation:** Google Imagen 4 / Gemini 2.5 Flash (auto-fallback)
- **Orchestration:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with Agent Teams
- **Inspiration:** PaperBanana (Critic-Visualizer-Loop)

## License

[MIT](LICENSE)
