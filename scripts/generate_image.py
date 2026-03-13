#!/usr/bin/env python3
"""
PresentationBanana — Gemini Image Generator
============================================
Generates images via Google Imagen / Gemini API.
Supports both slide-type presets and custom dimensions.

Usage:
    # Slide preset (for presentations):
    python generate_image.py --slide 1 --prompt "..." --version 1 --slide-type content

    # Custom size (for standalone images):
    python generate_image.py --slide 1 --prompt "..." --version 1 --width 3440 --height 1440

    # Custom size with name:
    python generate_image.py --slide 1 --prompt "..." --version 1 --width 1920 --height 1080 --name wallpaper

Slide types → aspect ratio → output size:
    content  →  9:16  →  640 × 900 px
    title    →  9:16  →  720 × 900 px
    closing  →  9:16  →  720 × 900 px
    section  →  16:9  →  1280 × 720 px
    visual   →  16:9  →  1280 × 720 px  (central illustration, replaces bullet text)
    icon     →  1:1   →  256 × 256 px

Custom sizes: any WxH — closest Gemini aspect ratio is auto-selected.
Supported Gemini ratios: 1:1, 3:4, 4:3, 9:16, 16:9

Output:
    JSON to stdout: {"ok": true, "path": "...", "slide": 1, "size": [640, 900]}
    Image saved to: output/images/v{version}/{name}_s{N}_{type}.png

Requirements:
    pip install google-genai pillow
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Load .env file if present (so GOOGLE_API_KEY can live in .env)
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if value and not os.environ.get(key):
                os.environ[key] = value


def _get_project_slug() -> str:
    """Derive a URL-safe slug from workspace/slide_structure.md topic."""
    structure_file = Path(__file__).parent.parent / "workspace" / "slide_structure.md"
    try:
        content = structure_file.read_text(encoding="utf-8")
        m = re.search(r'\*\*Topic:\*\*\s*(.+)', content)
        if not m:
            return "presentation"
        topic = m.group(1).strip()
        # Take part before em-dash, colon or comma
        topic = re.split(r'[—–,:]', topic)[0].strip()
        # German umlaut replacements
        for old, new in [('ä','ae'),('ö','oe'),('ü','ue'),('Ä','Ae'),('Ö','Oe'),('Ü','Ue'),('ß','ss')]:
            topic = topic.replace(old, new)
        # Lowercase, split words, take first 4
        words = topic.lower().split()[:4]
        slug = '-'.join(re.sub(r'[^a-z0-9]', '', w) for w in words)
        slug = re.sub(r'-+', '-', slug).strip('-')
        return slug or "presentation"
    except Exception:
        return "presentation"

# ── Size config per slide type ─────────────────────────────────────────────────
SLIDE_TYPE_CONFIG = {
    "content": {"aspect": "9:16", "resize": (640, 900)},
    "title":   {"aspect": "9:16", "resize": (720, 900)},
    "closing": {"aspect": "9:16", "resize": (720, 900)},
    "section": {"aspect": "16:9", "resize": (1280, 720)},
    "visual":  {"aspect": "16:9", "resize": (1280, 720)},  # central illustration slide
    "icon":    {"aspect": "1:1",  "resize": (256, 256)},
    "default": {"aspect": "9:16", "resize": (640, 900)},
}

# Gemini-supported aspect ratios with their numeric values
GEMINI_RATIOS = {
    "1:1":  1.0,
    "3:4":  3 / 4,
    "4:3":  4 / 3,
    "9:16": 9 / 16,
    "16:9": 16 / 9,
}


def _closest_aspect_ratio(w: int, h: int) -> str:
    """Pick the Gemini aspect ratio closest to the given dimensions."""
    target = w / h
    return min(GEMINI_RATIOS, key=lambda r: abs(GEMINI_RATIOS[r] - target))


ASPECT_SUFFIX = {
    "9:16": (
        "Vertical portrait format, professional quality, "
        "no text, no watermarks, clean composition, suitable for presentation panel."
    ),
    "16:9": (
        "Widescreen 16:9 format, cinematic, atmospheric, "
        "no text, no watermarks, full-bleed background quality."
    ),
    "1:1": (
        "Square format, flat minimal icon style, single concept, "
        "clean simple design, bold shape, no text, no labels, no watermarks, "
        "isolated symbol on solid dark background, professional icon aesthetic."
    ),
}


def resize_image(img, target: tuple):
    from PIL import Image
    return img.resize(target, Image.LANCZOS)


def generate(slide_num: int, prompt: str, version: int, slide_type: str,
             icon_index=None, width=None, height=None, aspect_ratio=None,
             name=None) -> dict:

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"ok": False, "error": "GOOGLE_API_KEY not set"}

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return {"ok": False, "error": "Run: pip install google-genai pillow"}

    # Custom size mode: --width + --height override slide-type presets
    if width and height:
        target = (width, height)
        aspect = aspect_ratio if aspect_ratio else _closest_aspect_ratio(width, height)
    else:
        cfg = SLIDE_TYPE_CONFIG.get(slide_type, SLIDE_TYPE_CONFIG["default"])
        aspect = aspect_ratio if aspect_ratio else cfg["aspect"]
        target = cfg["resize"]

    out_dir = Path(__file__).parent.parent / "output" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = name if name else _get_project_slug()
    if icon_index is not None:
        out_path = out_dir / f"{slug}_s{slide_num:02d}_icon_{icon_index}_v{version}.png"
    else:
        label = f"{target[0]}x{target[1]}" if width and height else slide_type
        out_path = out_dir / f"{slug}_s{slide_num:02d}_{label}_v{version}.png"

    enhanced_prompt = f"{prompt}. {ASPECT_SUFFIX.get(aspect, ASPECT_SUFFIX['16:9'])}"

    client = genai.Client(api_key=api_key)

    # Try Imagen 4 first
    try:
        result = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=enhanced_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect,
            ),
        )

        if not result.generated_images:
            raise RuntimeError("No images returned from Imagen 3")

        img_bytes = result.generated_images[0].image.image_bytes
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(img_bytes))
        img = resize_image(img, target)
        img.save(str(out_path), "PNG", optimize=True)

        return {
            "ok":      True,
            "path":    str(out_path),
            "slide":   slide_num,
            "version": version,
            "size":    list(target),
            "aspect":  aspect,
            "model":   "imagen-4",
        }

    except Exception as e:
        imagen_error = str(e)

    # Fallback: Gemini 2.0 Flash image generation
    try:
        from PIL import Image
        import io

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                img = Image.open(io.BytesIO(part.inline_data.data))
                img = resize_image(img, target)
                img.save(str(out_path), "PNG", optimize=True)
                return {
                    "ok":      True,
                    "path":    str(out_path),
                    "slide":   slide_num,
                    "version": version,
                    "size":    list(target),
                    "aspect":  aspect,
                    "model":   "gemini-flash-fallback",
                }

        return {
            "ok":    False,
            "error": f"imagen-3 failed: {imagen_error} | flash: no image in response",
            "slide": slide_num,
        }

    except Exception as e2:
        return {
            "ok":    False,
            "error": f"imagen-3 failed: {imagen_error} | flash failed: {str(e2)}",
            "slide": slide_num,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate an image (slide preset or custom size)"
    )
    parser.add_argument("--slide",      type=int,  required=True,
                        help="Image number (1, 2, 3...)")
    parser.add_argument("--prompt",     type=str,  required=True)
    parser.add_argument("--version",    type=int,  default=1)
    parser.add_argument("--slide-type", type=str,  default="content",
                        choices=list(SLIDE_TYPE_CONFIG.keys()),
                        help="Slide preset (ignored when --width/--height set)")
    parser.add_argument("--icon-index", type=int,  default=None)
    parser.add_argument("--width",      type=int,  default=None,
                        help="Custom width in px (e.g. 3440)")
    parser.add_argument("--height",     type=int,  default=None,
                        help="Custom height in px (e.g. 1440)")
    parser.add_argument("--aspect-ratio", type=str, default=None,
                        choices=list(GEMINI_RATIOS.keys()),
                        help="Override Gemini aspect ratio")
    parser.add_argument("--name",       type=str,  default=None,
                        help="Filename prefix (e.g. 'wallpaper', 'banner')")
    args = parser.parse_args()

    if (args.width is None) != (args.height is None):
        parser.error("--width and --height must be used together")

    result = generate(args.slide, args.prompt, args.version, args.slide_type,
                      icon_index=args.icon_index, width=args.width,
                      height=args.height, aspect_ratio=args.aspect_ratio,
                      name=args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
