"""
Render the landing-page HTML output — a single .html file containing each
page block as a self-contained Tailwind <section> the buyer can paste into
their Shopify section, PageFly block, or custom theme.

This script handles the WRAPPING — the header comment, the per-block comment
boundaries, the file structure. The HTML for each block's content comes
already-rendered from the LLM driving the skill, following the conventions
in templates/html-conventions.md.

Input JSON shape (closely mirrors the .docx brief input but with rendered
HTML strings instead of structured copy):
    {
      "page_name": "...",
      "page_type": "pdp | collection | marketing_lp | about",
      "brand_name": "...",
      "framework": "PAS",
      "generated_at": "2026-05-21",
      "blocks": [
        {
          "name": "HERO",
          "class_suffix": "hero",          # produces class="lp-hero"
          "purpose": "...",
          "html": "<div class='...'>...full block HTML...</div>"
        },
        ...
      ],
      "alternate_heroes": [
        {"name": "Hero A — Problem-aware", "class_suffix": "hero-alt-a", "html": "<div>...</div>"},
        ...
      ]
    }

The script wraps each block's html in a <section class="lp-{class_suffix}">
container with a navigation comment header. Output is plain UTF-8 text.
"""

import json
import sys
from pathlib import Path


PAGE_TYPE_DISPLAY = {
    "pdp": "Product Detail Page",
    "collection": "Collection / Category Page",
    "marketing_lp": "Marketing Landing Page",
    "about": "About / Brand Story Page",
}


def _file_header(data: dict) -> str:
    page_type = data.get("page_type", "pdp")
    type_display = PAGE_TYPE_DISPLAY.get(page_type, page_type)
    return f"""<!--
  Landing Page HTML — {data.get('page_name', 'Untitled')}
  Generated {data.get('generated_at', '')} · Brand: {data.get('brand_name', '')} · Page type: {type_display}
  Framework: {data.get('framework', '—')}

  USAGE:
  - Each <section> below is self-contained — copy and paste any block into your page builder.
  - Tailwind required. Quick test: add <script src="https://cdn.tailwindcss.com"></script> to your theme's <head>.
  - Replace REPLACE_WITH_YOUR_IMAGE placeholders with your real image URLs.
  - Edit alt text on every image to be shopper-facing (the placeholder alt is instructional).
  - All blocks are mobile-first and responsive.

  TABLE OF CONTENTS:
"""


def _file_toc(blocks: list[dict], alternates: list[dict]) -> str:
    lines = []
    for i, block in enumerate(blocks, 1):
        lines.append(f"    {i}. {block.get('name', 'BLOCK')}")
    if alternates:
        lines.append("    Alternate hero blocks (for A/B testing):")
        for alt in alternates:
            lines.append(f"      - {alt.get('name', 'ALTERNATE HERO')}")
    lines.append("-->\n")
    return "\n".join(lines)


def _block_header_comment(block: dict, is_alternate: bool = False) -> str:
    name = block.get("name", "BLOCK")
    purpose = block.get("purpose", "")
    if is_alternate:
        return (
            f"<!-- =================================================================\n"
            f"     ALTERNATE {name}\n"
            f"     For A/B testing against the main hero above.\n"
            f"     ================================================================= -->\n"
        )
    purpose_line = f"     Conversion job: {purpose}\n" if purpose else ""
    return (
        f"<!-- =================================================================\n"
        f"     {name}\n"
        f"{purpose_line}"
        f"     ================================================================= -->\n"
    )


def _render_block(block: dict, is_alternate: bool = False) -> str:
    """Wrap the block's HTML in a <section> with proper class and comment header."""
    class_suffix = block.get("class_suffix", "block")
    html = block.get("html", "<!-- block HTML missing -->")
    header = _block_header_comment(block, is_alternate=is_alternate)
    # If html doesn't already start with <section>, wrap it
    html_stripped = html.strip()
    if html_stripped.startswith("<section"):
        # Trust the LLM-supplied wrapper
        return f"{header}{html_stripped}\n"
    # Otherwise wrap
    section_open = (
        f'<section class="lp-{class_suffix} w-full py-12 md:py-20 px-4 md:px-8">\n'
        f'  <div class="max-w-7xl mx-auto">\n'
    )
    section_close = "  </div>\n</section>\n"
    # Indent the inner HTML by 4 spaces
    indented = "\n".join(("    " + line if line.strip() else line) for line in html_stripped.split("\n"))
    return f"{header}{section_open}{indented}\n{section_close}"


def render(data: dict, output_path: Path) -> Path:
    blocks = data.get("blocks", []) or []
    alternates = data.get("alternate_heroes", []) or []

    parts: list[str] = []
    parts.append(_file_header(data))
    parts.append(_file_toc(blocks, alternates))

    for block in blocks:
        parts.append(_render_block(block, is_alternate=False))
        parts.append("\n")

    if alternates:
        parts.append(
            "\n<!-- =================================================================\n"
            "     ALTERNATE HERO BLOCKS (A/B TEST CANDIDATES)\n"
            "     Each alternate is independently runnable in your A/B testing tool.\n"
            "     Copy one at a time. Don't ship multiple heroes live simultaneously.\n"
            "     ================================================================= -->\n\n"
        )
        for alt in alternates:
            parts.append(_render_block(alt, is_alternate=True))
            parts.append("\n")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(parts), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_html_sections.py <html_input_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
