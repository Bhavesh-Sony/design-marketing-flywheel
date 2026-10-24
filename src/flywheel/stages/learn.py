from __future__ import annotations

from flywheel.state import CycleState


def refresh_from_performance(state: CycleState, campaign_lift: float = 0.0) -> CycleState:
    """Close the loop: campaign performance adjusts the next-cycle prior."""
    if not state.released_brief:
        state.learning_update = {
            "applied": False,
            "reason": "No released brief. Learning does not run on a draft.",
        }
        return state

    featured = state.released_brief["featured_combination"]
    state.learning_update = {
        "applied": True,
        "attributes": featured,
        "prior_adjustment": round(campaign_lift, 3),
        "next_cycle": "Write the lift back into the sell-through prior for this combination.",
    }
    state.notes.append("Learning loop recorded a prior adjustment for the next season.")
    return state
