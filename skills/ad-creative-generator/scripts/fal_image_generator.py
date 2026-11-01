"""
Generate A+ Content module images via the Fal AI API.

Requires the buyer's Fal AI key (loaded from <plugin-root>/.config/the-ecommerce-seller.config.json
at config.api_keys.fal_ai). When no key is present, the calling skill should fall
back to outputting Canva briefs instead — this script will return None and log a
clear message rather than failing.

Default model: flux/dev (clean photographic output, handles composition well).
Override via the `model` arg.

Usage from another script:
    from fal_image_generator import generate_image, generate_batch, is_key_present

    if not is_key_present():
        # fall back to Canva briefs
        ...

    image_path = generate_image(
        prompt="A hand-thrown ceramic pour-over on a wooden counter, soft morning light...",
        width=1940, height=1200,
        output_path=Path("/path/to/output/aplus_hero.png"),
        seed=42,  # use the same seed across a module set to maintain visual consistency
    )

CLI:
    python fal_image_generator.py "your prompt here" out.png 1940 1200
    python fal_image_generator.py --check-key   # quick key presence check
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


CONFIG_FILENAME = "the-ecommerce-seller.config.json"
CONFIG_SUBDIR = ".config"

DEFAULT_MODEL = "fal-ai/flux/dev"
DEFAULT_NEGATIVE = (
    "text, watermark, logo overlay, signature, price tag, promotional badge, "
    "sale sticker, competitor branding, distorted proportions, extra limbs, "
    "surreal artifacts, low quality, blurry"
)


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate plugin root (no plugin.json found walking up from "
        f"{here})."
    )


def _config_path() -> Path:
    return find_plugin_root() / CONFIG_SUBDIR / CONFIG_FILENAME


def get_fal_key() -> str | None:
    """Returns the Fal AI key from config, or from the FAL_KEY env var as fallback. None if missing."""
    # Env var takes precedence (useful for CI / testing)
    env_key = os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_KEY")
    if env_key:
        return env_key.strip()
    path = _config_path()
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            cfg = json.load(f)
        key = (cfg.get("api_keys", {}) or {}).get("fal_ai", "")
        return key.strip() if isinstance(key, str) and key.strip() else None
    except (json.JSONDecodeError, OSError):
        return None


def is_key_present() -> bool:
    return get_fal_key() is not None


def _call_fal(prompt: str, model: str, width: int, height: int, seed: int | None, negative_prompt: str) -> dict:
    """
    Submit a generation request to Fal. Uses the simple synchronous-style
    endpoint. Returns the parsed JSON response.
    """
    key = get_fal_key()
    if not key:
        raise RuntimeError(
            "Fal AI key not found. Add it via plugin onboarding (config.api_keys.fal_ai) "
            "or export FAL_KEY in your environment."
        )

    url = f"https://fal.run/{model}"
    body: dict = {
        "prompt": prompt,
        "image_size": {"width": width, "height": height},
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
        "num_images": 1,
        "enable_safety_checker": True,
        "negative_prompt": negative_prompt,
    }
    if seed is not None:
        body["seed"] = seed

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Key {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Fal API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Fal API network error: {exc.reason}") from exc


def _download_image(image_url: str, output_path: Path) -> Path:
    """Download a generated image URL to the local output path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    output_path.write_bytes(data)
    return output_path


def generate_image(
    prompt: str,
    width: int,
    height: int,
    output_path: Path,
    seed: int | None = None,
    model: str = DEFAULT_MODEL,
    negative_prompt: str = DEFAULT_NEGATIVE,
    retries: int = 1,
) -> Path | None:
    """
    Generate one image and save to output_path. Returns the saved path on success,
    None on failure. Caller decides whether to fall back to a Canva brief on None.
    """
    full_prompt = prompt.strip()
    last_exc: Exception | None = None
    for attempt in range(1 + retries):
        try:
            response = _call_fal(full_prompt, model, width, height, seed, negative_prompt)
            images = response.get("images") or []
            if not images:
                raise RuntimeError(f"Fal returned no images. Response keys: {list(response.keys())}")
            image_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
            if not image_url:
                raise RuntimeError("Fal response did not include an image URL")
            return _download_image(image_url, output_path)
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                print(f"[fal_image_generator] Attempt {attempt + 1} failed: {exc}. Retrying...", file=sys.stderr)
                time.sleep(1.5)
            else:
                print(f"[fal_image_generator] All {1 + retries} attempts failed for {output_path.name}: {exc}", file=sys.stderr)
    return None


def generate_batch(
    specs: list[dict],
    output_dir: Path,
    base_seed: int | None = None,
) -> list[dict]:
    """
    Generate a batch of images. Each spec is a dict:
        {
          "name": "module-1-hero",
          "prompt": "...",
          "width": 1940,
          "height": 1200,
          "filename": "aplus_module-1-hero.png",    # optional; defaults to {name}.png
          "seed_offset": 0,                          # optional; added to base_seed
        }
    Returns list of result dicts with success flag + path.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    for spec in specs:
        name = spec.get("name", "image")
        filename = spec.get("filename") or f"{name}.png"
        out_path = output_dir / filename
        seed = None
        if base_seed is not None:
            seed = base_seed + int(spec.get("seed_offset", 0))
        result_path = generate_image(
            prompt=spec.get("prompt", ""),
            width=int(spec.get("width", 1024)),
            height=int(spec.get("height", 1024)),
            output_path=out_path,
            seed=seed,
        )
        results.append({
            "name": name,
            "filename": filename,
            "success": result_path is not None,
            "path": str(result_path) if result_path else None,
        })
    return results


def _cli():
    parser = argparse.ArgumentParser(description="Generate A+ Content images via Fal AI.")
    parser.add_argument("--check-key", action="store_true", help="Check whether a Fal key is configured and exit.")
    parser.add_argument("prompt", nargs="?", default=None, help="Generation prompt")
    parser.add_argument("output", nargs="?", default=None, help="Output PNG path")
    parser.add_argument("width", nargs="?", default=1024, type=int, help="Image width")
    parser.add_argument("height", nargs="?", default=1024, type=int, help="Image height")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed")
    args = parser.parse_args()

    if args.check_key:
        if is_key_present():
            print("Fal AI key configured: yes")
            sys.exit(0)
        else:
            print("Fal AI key configured: no")
            sys.exit(1)

    if not args.prompt or not args.output:
        parser.error("Provide a prompt and output path, or use --check-key.")

    out_path = generate_image(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        output_path=Path(args.output),
        seed=args.seed,
    )
    if out_path:
        print(f"Wrote {out_path}")
    else:
        print("Generation failed. See errors above.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    _cli()
