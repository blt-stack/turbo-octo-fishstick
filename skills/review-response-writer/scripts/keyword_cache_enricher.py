"""
Enricher for the shared keywords.json cache.

Skill #2 (Listing SEO Optimizer) is the primary writer of the keyword cache.
This script appends review-mined keyword candidates to the existing artifact
without overwriting skill #2's original keyword list.

Path convention (must match skill #2's keyword_artifact_writer.py):
    <plugin-root>/.cache/keywords/{product-identifier}.json

How enrichment works:
1. Load existing artifact at cache path (created by skill #2)
2. If no artifact exists, create a minimal stub artifact so review mining
   doesn't fail (skill #2 will pick up and rewrite when next run)
3. Append review-mined keywords to artifact["keywords_ranked"] with source tag
4. Re-save artifact

The original keywords from skill #2 stay first in the list (higher rank).
Review-mined keywords get appended at lower rank to indicate they're
supplementary signal, not primary SEO terms.

Schema for review-mined keyword entries:
    {
      "keyword": "the grip feels balanced",
      "rank": 11,
      "source": "review-mining",
      "occurrences_in_reviews": 5,
      "first_observed": "2026-05-10",
      "recommended_placement": ["product_description_body", "ad_creative_testimonial"],
      "evidence_reviews": ["judge_me:123", "judge_me:128"]
    }

Usage:
    from keyword_cache_enricher import enrich_keywords

    enrich_keywords(
        product_identifier="river-stone-pour-over",
        product_name="River Stone Pour-Over",
        new_keywords=[
            {"keyword": "feels balanced", "occurrences": 5, "evidence": ["judge_me:123"]},
        ]
    )
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = ".cache/keywords"


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        f"Could not locate plugin root walking up from {here}."
    )


def cache_dir() -> Path:
    return find_plugin_root() / CACHE_SUBDIR


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-product"


def cache_path_for(product_identifier: str) -> Path:
    return cache_dir() / f"{product_identifier}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _empty_stub_artifact(product_identifier: str, product_name: str) -> dict:
    return {
        "product_identifier": product_identifier,
        "product_name": product_name,
        "generated_at": _now_iso(),
        "source": "review-response-writer-stub",
        "_note": (
            "Stub artifact created by review-response-writer's keyword enrichment. "
            "Run Listing SEO Optimizer (skill #2) to populate primary keyword research."
        ),
        "keywords_ranked": [],
    }


def load_artifact(product_identifier: str) -> dict | None:
    path = cache_path_for(product_identifier)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[keyword_cache_enricher] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def _phrase_already_present(existing_keywords: list[dict], phrase: str) -> bool:
    phrase_norm = phrase.strip().lower()
    for k in existing_keywords:
        if (k.get("keyword") or "").strip().lower() == phrase_norm:
            return True
    return False


def enrich_keywords(
    product_identifier: str,
    product_name: str,
    new_keywords: list[dict],
) -> Path:
    """
    Append review-mined keywords to the existing keyword artifact.

    Each new_keywords entry should look like:
      {
        "keyword": "feels balanced",
        "occurrences": 5,
        "first_observed": "2026-05-10",
        "evidence": ["judge_me:123", "judge_me:128"]
      }

    The enricher computes the rank slot (next available below existing keywords),
    auto-stamps source="review-mining", and dedupes by keyword phrase.
    """
    path = cache_path_for(product_identifier)
    path.parent.mkdir(parents=True, exist_ok=True)

    artifact = load_artifact(product_identifier) or _empty_stub_artifact(product_identifier, product_name)
    artifact.setdefault("keywords_ranked", [])

    existing = artifact["keywords_ranked"]
    next_rank = max((k.get("rank", 0) for k in existing), default=0) + 1

    added = 0
    for nk in (new_keywords or []):
        phrase = (nk.get("keyword") or "").strip()
        if not phrase:
            continue
        if _phrase_already_present(existing, phrase):
            continue
        entry = {
            "keyword": phrase,
            "rank": next_rank,
            "source": "review-mining",
            "occurrences_in_reviews": nk.get("occurrences", 1),
            "first_observed": nk.get("first_observed", _now_iso()[:10]),
            "evidence_reviews": nk.get("evidence", []),
            "recommended_placement": nk.get(
                "recommended_placement",
                ["product_description_body", "ad_creative_testimonial"],
            ),
        }
        existing.append(entry)
        next_rank += 1
        added += 1

    artifact["last_enriched_at"] = _now_iso()
    artifact["last_enriched_by"] = "review-response-writer"

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def review_mined_keywords(artifact: dict) -> list[dict]:
    """Return only the review-mined keywords from an artifact (useful for audit)."""
    if not artifact:
        return []
    return [k for k in artifact.get("keywords_ranked", []) if k.get("source") == "review-mining"]


def list_cached() -> list[str]:
    d = cache_dir()
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        cached = list_cached()
        if not cached:
            print("No keyword artifacts cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(cached)} cached keyword artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "review_only":
        if len(sys.argv) < 3:
            print("Usage: keyword_cache_enricher.py review_only <product_identifier>")
            sys.exit(1)
        artifact = load_artifact(sys.argv[2])
        if not artifact:
            print(f"No artifact for '{sys.argv[2]}'")
            sys.exit(1)
        mined = review_mined_keywords(artifact)
        if not mined:
            print("No review-mined keywords in this artifact.")
        else:
            print(f"{len(mined)} review-mined keyword(s):")
            for k in mined:
                print(f"  [rank {k.get('rank', '?')}] \"{k.get('keyword', '')}\" — {k.get('occurrences_in_reviews', '?')} occurrences")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: keyword_cache_enricher.py [list | review_only <id>]")
        sys.exit(1)
