"""Greedy vs optimal fleet assignment, pure standard library.

For a small fleet, brute-force optimal assignment (all permutations)
is compared with the greedy nearest-vehicle assignment used in
fleet_orchestrator.py. This shows the optimization gap on synthetic
data: greedy is fast, optimal is better but only feasible for
small fleets, which is exactly why real dispatch uses heuristics
and solvers. Not a claim of deep optimization expertise, and not
a production solver.
"""
import itertools
import random
from fleet_orchestrator import dist


def compare(n=8, seed=42):
    rng = random.Random(seed)
    vehicles = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]
    riders = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]
    # Greedy: assign each rider in order to its nearest free vehicle.
    free = list(range(n))
    greedy_total = 0.0
    for r in riders:
        v = min(free, key=lambda i: dist(vehicles[i][0], vehicles[i][1], r[0], r[1]))
        greedy_total += dist(vehicles[v][0], vehicles[v][1], r[0], r[1])
        free.remove(v)
    # Optimal: best permutation of vehicles to riders.
    optimal_total = min(
        sum(dist(vehicles[v][0], vehicles[v][1], riders[i][0], riders[i][1])
            for i, v in enumerate(perm))
        for perm in itertools.permutations(range(n)))
    return {
        "vehicles": n,
        "riders": n,
        "greedy_total_distance": round(greedy_total, 2),
        "optimal_total_distance": round(optimal_total, 2),
        "greedy_gap_pct": round((greedy_total - optimal_total) / optimal_total * 100, 2),
    }


if __name__ == "__main__":
    print(compare())
