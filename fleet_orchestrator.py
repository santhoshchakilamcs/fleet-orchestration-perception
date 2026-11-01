"""Fleet orchestration simulator, pure standard library.

Simulates a robotaxi fleet on a grid: riders appear at random
locations, vehicles are assigned greedily to the nearest rider,
idle vehicles are staged toward demand hotspots, and trips are
completed. Returns utilization, average wait, completed trips,
and empty miles. This is a teaching simulator on SYNTHETIC data,
not Zoox data and not a production dispatch system.
"""
import random
from dataclasses import dataclass


@dataclass
class Vehicle:
    id: int
    x: float
    y: float
    busy_until: int = 0
    trips: int = 0
    empty_miles: float = 0.0


@dataclass
class Rider:
    id: int
    x: float
    y: float
    dx: float
    dy: float
    arrived: int
    picked_up: int = -1


def dist(ax, ay, bx, by):
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def simulate(n_vehicles=20, n_riders=100, steps=200, seed=42, grid=10.0):
    rng = random.Random(seed)
    # Demand hotspots: two corners of the grid get more riders.
    hotspots = [(2.0, 2.0), (8.0, 8.0)]
    vehicles = [Vehicle(i, rng.uniform(0, grid), rng.uniform(0, grid))
                for i in range(n_vehicles)]
    riders = []
    for i in range(n_riders):
        hx, hy = rng.choice(hotspots)
        riders.append(Rider(i,
                            max(0, min(grid, hx + rng.gauss(0, 1.5))),
                            max(0, min(grid, hy + rng.gauss(0, 1.5))),
                            rng.uniform(0, grid), rng.uniform(0, grid),
                            arrived=rng.randint(0, steps // 2)))
    waiting = []
    completed = 0
    waits = []
    for t in range(steps):
        for r in riders:
            if r.arrived == t:
                waiting.append(r)
        # Assign nearest available vehicle to each waiting rider.
        for r in list(waiting):
            free = [v for v in vehicles if v.busy_until <= t]
            if not free:
                break
            v = min(free, key=lambda v: dist(v.x, v.y, r.x, r.y))
            d_pickup = dist(v.x, v.y, r.x, r.y)
            d_trip = dist(r.x, r.y, r.dx, r.dy)
            v.empty_miles += d_pickup
            v.busy_until = t + int((d_pickup + d_trip) * 2) + 1
            v.trips += 1
            v.x, v.y = r.dx, r.dy
            r.picked_up = t
            waits.append(t - r.arrived)
            waiting.remove(r)
            completed += 1
        # Stage idle vehicles toward the nearest hotspot.
        for v in vehicles:
            if v.busy_until <= t:
                hx, hy = min(hotspots, key=lambda h: dist(v.x, v.y, h[0], h[1]))
                v.x += (hx - v.x) * 0.1
                v.y += (hy - v.y) * 0.1
    busy_time = sum(v.trips for v in vehicles)
    return {
        "vehicles": n_vehicles,
        "riders": n_riders,
        "completed_trips": completed,
        "completion_rate": completed / max(1, n_riders),
        "avg_wait_steps": sum(waits) / max(1, len(waits)),
        "total_empty_miles": round(sum(v.empty_miles for v in vehicles), 2),
        "trips_per_vehicle": round(busy_time / max(1, n_vehicles), 2),
        "unserved_riders": len(waiting),
    }


if __name__ == "__main__":
    print(simulate())
