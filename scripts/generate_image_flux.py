#!/usr/bin/env python3
"""
PresentationBanana — Flux Image Generator (Replicate)
====================================================
Generates images via Flux.1 Dev on Replicate API.

Usage:
    python generate_image_flux.py --slide 1 --prompt "..." --version 1 --width 2736 --height 1824 --name wallpaper

    # With negative prompt:
    python generate_image_flux.py --slide 1 --prompt "..." --negative "text, watermark, deformed" --version 1

Output:
    JSON to stdout: {"ok": true, "path": "...", "slide": 1, "size": [2736, 1824]}
    Image saved to: output/images/{name}_s{N}_{WxH}_v{V}.png
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Load .env file if present
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if value and not os.environ.get(key):
                os.environ[key] = value

# Preset sizes
PRESET_SIZES = {
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "1:1": (1024, 1024),
    "ultrawide": (3440, 1440),
    "fullhd": (1920, 1080),
    "2k": (2560, 1440),
    "surface": (2736, 1824),
}

# Flux Dev on Replicate supports these aspect ratios
ASPECT_RATIOS = [
    "1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21",
]


def _best_aspect_ratio(width: int, height: int) -> str:
    """Find the closest supported aspect ratio for the given dimensions."""
    target = width / height
    best = None
    best_diff = float("inf")
    for ar in ASPECT_RATIOS:
        w, h = map(int, ar.split(":"))
        diff = abs(target - w / h)
        if diff < best_diff:
            best_diff = diff
            best = ar
    return best


def generate(slide_num: int, prompt: str, version: int, width: int, height: int,
             name: str = "flux-image", negative: str = "", steps: int = 28,
             guidance: float = 3.5) -> dict:

    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        return {"ok": False, "error": "REPLICATE_API_TOKEN not set in .env"}

    try:
        import replicate
    except ImportError:
        return {"ok": False, "error": "Run: pip install replicate"}

    out_dir = Path(__file__).parent.parent / "output" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}_s{slide_num:02d}_{width}x{height}_v{version}.png"

    aspect_ratio = _best_aspect_ratio(width, height)

    input_params = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_inference_steps": steps,
        "guidance": guidance,
        "output_format": "png",
        "output_quality": 100,
    }

    if negative:
        input_params["prompt"] = f"{prompt}. Avoid: {negative}"

    try:
        print(f"Sende an Replicate (Flux Dev, {aspect_ratio})...", file=sys.stderr)
        output = replicate.run(
            "black-forest-labs/flux-dev",
            input=input_params,
        )

        # output is a FileOutput or list of FileOutput
        if isinstance(output, list):
            image_url = output[0]
        else:
            image_url = output

        # Download the image
        import urllib.request
        urllib.request.urlretrieve(str(image_url), str(out_path))

        # Resize to exact requested dimensions if needed
        from PIL import Image
        img = Image.open(out_path)
        if img.size != (width, height):
            img = img.resize((width, height), Image.LANCZOS)
            img.save(out_path)

        actual_size = (width, height)

        return {
            "ok": True,
            "path": str(out_path),
            "slide": slide_num,
            "version": version,
            "size": list(actual_size),
            "aspect_ratio": aspect_ratio,
            "model": "flux-1-dev (replicate)",
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Flux generation failed: {str(e)}",
            "slide": slide_num,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate an image via Flux Dev on Replicate"
    )
    parser.add_argument("--slide", type=int, required=True,
                        help="Image number (1, 2, 3...)")
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--negative", type=str, default="",
                        help="Negative prompt (things to avoid)")
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--name", type=str, default="flux-image",
                        help="Filename prefix")
    parser.add_argument("--steps", type=int, default=28,
                        help="Inference steps (default: 28)")
    parser.add_argument("--guidance", type=float, default=3.5,
                        help="Guidance scale (default: 3.5)")
    parser.add_argument("--preset", type=str, default=None,
                        choices=list(PRESET_SIZES.keys()),
                        help="Preset size (overrides --width/--height)")
    args = parser.parse_args()

    if args.preset:
        args.width, args.height = PRESET_SIZES[args.preset]

    result = generate(args.slide, args.prompt, args.version, args.width, args.height,
                      name=args.name, negative=args.negative, steps=args.steps,
                      guidance=args.guidance)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
