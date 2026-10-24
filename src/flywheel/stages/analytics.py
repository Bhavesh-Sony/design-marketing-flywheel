from __future__ import annotations

from flywheel.state import CycleState


def score_combinations(state: CycleState) -> CycleState:
    """Join trend velocity with a simple sell-through prior from the signal payload."""
    priors = {
        tuple(sorted(signal.get("attributes", {}).items())): float(signal.get("sell_through", 0.4))
        for signal in state.signals
        if signal.get("attributes")
    }
    scored = []
    for trend in state.trend_scores:
        key = tuple(sorted(trend["attributes"].items()))
        sell_through = priors.get(key, 0.45)
        alignment = 1.0 if trend["velocity"] == "peak" else 0.7 if trend["velocity"] == "emerging" else 0.3
        scored.append(
            {
                "attributes": trend["attributes"],
                "velocity": trend["velocity"],
                "sell_through_prior": sell_through,
                "alignment_score": round(0.6 * alignment + 0.4 * sell_through, 3),
            }
        )
    scored.sort(key=lambda row: row["alignment_score"], reverse=True)
    state.combination_scores = scored
    state.notes.append("Ranked attribute combinations by trend alignment and sell-through prior.")
    return state
