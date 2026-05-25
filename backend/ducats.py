"""Loader for the pre-built ducat lookup table from data/ducats.json."""

import json
from pathlib import Path

_DATA_FILE = Path(__file__).parent.parent / "data" / "ducats.json"


def load_ducats() -> dict[str, int]:
    """Read data/ducats.json and return a {item_name: ducat_value} mapping.

    Keys are lowercase, single-space-normalized item component names.
    Values are positive integers representing Ducat Kiosk sell prices.

    Raises:
        FileNotFoundError: if data/ducats.json does not exist.
            Run `python -m backend.scripts.fetch_ducats` to generate it.
    """
    if not _DATA_FILE.exists():
        raise FileNotFoundError(
            f"data/ducats.json not found at {_DATA_FILE}. "
            "Run `python -m backend.scripts.fetch_ducats` to generate it."
        )
    with _DATA_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)
