"""Run one flywheel cycle with the sample signals."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flywheel.graph import run_cycle  # noqa: E402


def main() -> None:
    signals_path = Path(__file__).with_name("sample_signals.json")
    signals = json.loads(signals_path.read_text(encoding="utf-8"))
    state = run_cycle(signals, decision="approve", campaign_lift=0.12)
    print(json.dumps(state.to_dict(), indent=2))
    if state.gate_decision != "approve" or not state.released_brief:
        raise SystemExit("Cycle did not release a brief.")


if __name__ == "__main__":
    main()
