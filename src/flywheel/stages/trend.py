from __future__ import annotations

from collections import defaultdict

from flywheel.state import CycleState
from flywheel.taxonomy import map_phrase_to_attributes


def score_trends(state: CycleState) -> CycleState:
    """Map incoming signals onto the taxonomy and label velocity."""
    buckets: dict[tuple[str, ...], dict] = defaultdict(
        lambda: {"mentions": 0, "attributes": {}, "sources": []}
    )
    for signal in state.signals:
        mapped = map_phrase_to_attributes(signal.get("phrase", ""), state.taxonomy)
        if not mapped:
            continue
        key = tuple(sorted(mapped.items()))
        buckets[key]["mentions"] += int(signal.get("weight", 1))
        buckets[key]["attributes"] = mapped
        buckets[key]["sources"].append(signal.get("source", "unknown"))

    labels = state.taxonomy.get("velocity_labels", ["emerging", "peak", "declining"])
    scored = []
    for payload in buckets.values():
        mentions = payload["mentions"]
        if mentions >= 5:
            velocity = labels[1] if len(labels) > 1 else "peak"
        elif mentions >= 2:
            velocity = labels[0]
        else:
            velocity = labels[-1]
        scored.append({**payload, "velocity": velocity})

    scored.sort(key=lambda row: row["mentions"], reverse=True)
    state.trend_scores = scored
    state.notes.append(f"Scored {len(scored)} trend combinations from {len(state.signals)} signals.")
    return state
