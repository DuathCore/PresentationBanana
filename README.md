# PresentationBanana

**AI-powered PowerPoint presentations with Gemini Imagen + Claude Code.**

Takes a topic, PDF, or existing PPTX as input and generates a polished presentation with AI-generated images — fully automated through a Critic-Visualizer feedback loop.

## How It Works

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

Each iteration improves both images (re-generated with refined prompts) and slide text (tighter titles, sharper bullets). Typical improvement: +25–40% on the 5-point quality scale.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Google API Key

Go to [Google AI Studio](https://aistudio.google.com/apikey) and create an API key.

### 3. Configure Claude Code

Copy the example settings and add your key:

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

Edit `.claude/settings.local.json` and replace `YOUR-GOOGLE-API-KEY-HERE` with your actual key.

### 4. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

## Usage

### Quick Start (Claude Code Skill)

```bash
cd PresentationBanana
claude
```

Then type:
```
/presentation-banana
```

Claude asks for your topic, style, and slide count — then runs the full workflow.

### Image Generation Only

To generate standalone images (no PowerPoint), use:

```
/image-banana
```

Same Critic-Visualizer feedback loop, but focused purely on image quality. Supports single images, batches, and consistent series. Formats: 16:9, 9:16, 1:1.

### Input Options

Place your input in the `input/` folder:

- **`input/topic.md`** — Describe your topic (template included)
- **`input/document.pdf`** — Extract content from a PDF
- **`input/existing.pptx`** — Redesign an existing presentation

### Styles

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

### Generate a single image

```bash
python scripts/generate_image.py \
  --slide 3 \
  --prompt "modern boardroom meeting, warm lighting, professional" \
  --version 1
```

### Build presentation from slide_structure.md

```bash
python scripts/build_pptx.py --version 1 --style light-modern
```

## Output

```
output/
├── images/v1/          ← First iteration images
├── images/v2/          ← Refined images
└── presentations/      ← presentation_v1.pptx, presentation_v2.pptx
```

## Cost Estimates

| Item | Cost |
|------|------|
| Gemini Imagen (per image) | ~$0.04 |
| 10 slides x 2 iterations | ~$0.80 |
| Claude tokens (agent team) | ~$1–3 |
| **Total (10 slides)** | **$2–5** |

## Tech Stack

- **Presentation builder:** [python-pptx](https://python-pptx.readthedocs.io/)
- **Image generation:** Google Imagen 4 / Gemini 2.5 Flash
- **Orchestration:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with Agent Teams
- **Inspiration:** PaperBanana (Critic-Visualizer-Loop)

## License

[MIT](LICENSE)
