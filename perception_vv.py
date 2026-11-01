"""Perception verification and validation metrics, pure standard library.

Generates SYNTHETIC ground-truth objects and detector outputs with
controlled noise, matches them by centre distance, and computes
precision, recall, F1, false positives, false negatives, and
failure rates by synthetic condition (distance, rain, occlusion).
Also reports confidence calibration in bins. This is a metrics
demo on synthetic data, not Zoox perception data and not a
safety validation of any real system.
"""
import random


def evaluate(n_objects=500, noise=0.3, miss_rate=0.08, false_rate=0.10, seed=42):
    rng = random.Random(seed)
    conditions = ["near", "far", "rain", "occluded"]
    tp = fp = fn = 0
    by_condition = {c: {"tp": 0, "fp": 0, "fn": 0} for c in conditions}
    bins = {}
    for i in range(n_objects):
        cond = conditions[i % len(conditions)]
        if rng.random() < miss_rate:
            fn += 1
            by_condition[cond]["fn"] += 1
            continue
        # Noisy detection: centre offset grows with noise.
        offset = rng.gauss(0, noise)
        matched = abs(offset) < 1.0
        conf = max(0.05, min(0.99, 0.9 - abs(offset) * 0.2 + rng.gauss(0, 0.05)))
        b = round(conf * 10) / 10
        bins.setdefault(b, {"n": 0, "correct": 0})
        bins[b]["n"] += 1
        if matched:
            tp += 1
            by_condition[cond]["tp"] += 1
            bins[b]["correct"] += 1
        else:
            fp += 1
            by_condition[cond]["fp"] += 1
    fp += int(n_objects * false_rate)
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 2 * precision * recall / max(1e-9, precision + recall)
    failure = {}
    for c, d in by_condition.items():
        total = d["tp"] + d["fp"] + d["fn"]
        failure[c] = round((d["fp"] + d["fn"]) / max(1, total), 3)
    calibration = {str(k): round(v["correct"] / v["n"], 3) for k, v in sorted(bins.items())}
    return {
        "objects": n_objects,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "failure_rate_by_condition": failure,
        "confidence_calibration": calibration,
    }


if __name__ == "__main__":
    print(evaluate())
