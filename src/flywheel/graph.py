from __future__ import annotations

from typing import Any

from flywheel.gate import review_brief
from flywheel.stages.analytics import score_combinations
from flywheel.stages.brief import draft_brief
from flywheel.stages.learn import refresh_from_performance
from flywheel.stages.trend import score_trends
from flywheel.state import CycleState
from flywheel.taxonomy import load_taxonomy

# Node order mirrors a LangGraph StateGraph: trend -> analytics -> brief -> gate -> learn.
NODES = ("trend", "analytics", "brief", "gate", "learn")


def run_cycle(
    signals: list[dict[str, Any]],
    *,
    decision: str = "approve",
    campaign_lift: float = 0.0,
    taxonomy: dict[str, Any] | None = None,
) -> CycleState:
    """Run one scheduled cycle. Production would trigger this when new signals arrive."""
    state = CycleState(signals=signals, taxonomy=taxonomy or load_taxonomy())
    score_trends(state)
    score_combinations(state)
    draft_brief(state)
    review_brief(state, decision)
    refresh_from_performance(state, campaign_lift=campaign_lift)
    return state
