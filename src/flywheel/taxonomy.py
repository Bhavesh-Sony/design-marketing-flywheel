from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_TAXONOMY = Path(__file__).resolve().parents[2] / "config" / "taxonomy.yaml"


def load_taxonomy(path: Path | None = None) -> dict[str, Any]:
    with (path or DEFAULT_TAXONOMY).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def map_phrase_to_attributes(phrase: str, taxonomy: dict[str, Any]) -> dict[str, str]:
    """Map a free-text trend phrase onto known taxonomy values."""
    tokens = {token.strip(" ,.").lower() for token in phrase.replace("-", " ").split()}
    mapped: dict[str, str] = {}
    for attribute, values in taxonomy.get("attributes", {}).items():
        for value in values:
            parts = set(value.replace("-", " ").split())
            if parts <= tokens or value.replace("-", " ") in phrase.lower():
                mapped[attribute] = value
    return mapped
