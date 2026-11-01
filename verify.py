"""Verification script: runs both demos with fixed seeds and asserts sanity."""
from fleet_orchestrator import simulate
from perception_vv import evaluate

fleet = simulate()
perc = evaluate()
print("Fleet orchestration:", fleet)
print("Perception V&V:", perc)
assert 0 < fleet["completed_trips"] <= fleet["riders"]
assert 0 <= fleet["completion_rate"] <= 1
assert fleet["avg_wait_steps"] >= 0
assert 0 <= perc["precision"] <= 1 and 0 <= perc["recall"] <= 1
assert 0 <= perc["f1"] <= 1
assert perc["true_positives"] > 0
print("All sanity checks passed.")
