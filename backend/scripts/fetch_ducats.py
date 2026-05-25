"""Build-time script: fetches WFCD/warframe-items JSON and writes data/ducats.json.

Run once during project setup, then re-run after each Warframe release:
    python -m backend.scripts.fetch_ducats
"""

import json
import re
import sys
from pathlib import Path

import httpx

CATEGORIES = ["Warframes", "Primary", "Secondary", "Melee", "Sentinels"]
BASE_URL = "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "ducats.json"

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize(name: str) -> str:
    """Lowercase and collapse internal whitespace to single spaces."""
    return _WHITESPACE_RE.sub(" ", name.strip().lower())


def fetch_ducats() -> dict[str, int]:
    """Download all 5 category JSONs and return a merged {name: ducats} lookup."""
    lookup: dict[str, int] = {}
    with httpx.Client(timeout=30) as client:
        for category in CATEGORIES:
            url = f"{BASE_URL}/{category}.json"
            response = client.get(url)
            if response.status_code != 200:
                print(
                    f"ERROR: {url} returned HTTP {response.status_code}",
                    file=sys.stderr,
                )
                sys.exit(1)
            items: list[dict[str, object]] = response.json()
            for item in items:
                item_name: str = item.get("name", "")
                if "Prime" not in item_name:
                    continue
                for component in item.get("components", []):
                    ducats: int | None = component.get("ducats") or component.get(
                        "primeSellingPrice"
                    )
                    if ducats and isinstance(ducats, int) and ducats > 0:
                        full_name = f"{item_name} {component['name']}"
                        key = _normalize(full_name)
                        lookup[key] = ducats
    return lookup


def main() -> None:
    """Fetch ducat data and write to data/ducats.json."""
    lookup = fetch_ducats()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as fh:
        json.dump(lookup, fh, indent=2, sort_keys=True)
    print(f"wrote {len(lookup)} items to data/ducats.json")


if __name__ == "__main__":
    main()
