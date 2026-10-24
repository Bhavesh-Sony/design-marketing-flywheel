from __future__ import annotations

from flywheel.state import CycleState


def draft_brief(state: CycleState) -> CycleState:
    """Draft a design brief. Release happens only after the designer gate."""
    if not state.combination_scores:
        state.draft_brief = None
        state.notes.append("No combination scores, so no brief was drafted.")
        return state

    top = state.combination_scores[0]
    under = [row for row in state.combination_scores if row["alignment_score"] < 0.4][:3]
    state.draft_brief = {
        "status": "draft",
        "featured_combination": top["attributes"],
        "alignment_score": top["alignment_score"],
        "velocity": top["velocity"],
        "retire_or_review": [row["attributes"] for row in under],
        "instruction": "Draft only. A designer must approve before this brief is used.",
    }
    state.notes.append("Drafted a brief behind the review gate.")
    return state
