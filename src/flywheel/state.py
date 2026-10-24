from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CycleState:
    """Shared state that moves through the four stages and the review gate."""

    signals: list[dict[str, Any]]
    taxonomy: dict[str, Any]
    trend_scores: list[dict[str, Any]] = field(default_factory=list)
    combination_scores: list[dict[str, Any]] = field(default_factory=list)
    draft_brief: dict[str, Any] | None = None
    released_brief: dict[str, Any] | None = None
    gate_decision: str = "pending"
    learning_update: dict[str, Any] | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trend_scores": self.trend_scores,
            "combination_scores": self.combination_scores,
            "draft_brief": self.draft_brief,
            "released_brief": self.released_brief,
            "gate_decision": self.gate_decision,
            "learning_update": self.learning_update,
            "notes": self.notes,
        }
