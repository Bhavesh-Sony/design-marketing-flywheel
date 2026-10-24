from __future__ import annotations

from flywheel.state import CycleState


def review_brief(state: CycleState, decision: str) -> CycleState:
    """Human review gate. A brief is released only after an explicit approve."""
    allowed = {"approve", "revise", "hold"}
    if decision not in allowed:
        raise ValueError(f"decision must be one of {sorted(allowed)}")

    state.gate_decision = decision
    if decision == "approve" and state.draft_brief:
        state.released_brief = dict(state.draft_brief)
        state.released_brief["status"] = "released"
        state.notes.append("Designer approved the brief. Creative control stayed with the reviewer.")
    elif decision == "revise":
        state.released_brief = None
        state.notes.append("Designer sent the brief back. The next cycle must regenerate it.")
    else:
        state.released_brief = None
        state.notes.append("Designer held the brief. No recommendation left the system.")
    return state
