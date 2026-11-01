# Fleet Orchestration and Perception V&V

Two teaching demos built to match autonomous fleet data science work,
on synthetic data only.

## 1. Fleet orchestration simulator (`fleet_orchestrator.py`)
Riders appear near two demand hotspots on a grid. Vehicles are
assigned greedily to the nearest rider, idle vehicles stage toward
hotspots, and trips complete. Output: completed trips, completion
rate, average wait, empty miles, and trips per vehicle.

### Demand surge scenario (Streamlit fleet tab)
The fleet tab has a demand surge slider, 1.0x to 2.5x, for a
synthetic event-day scenario. It runs the baseline first, then
the same fleet at surge rider counts, so you can compare
completion rate, average wait, and unserved riders. A surge is
a scenario test, not a forecast of real demand. Verified example,
20 vehicles, seed 42: baseline 100 riders, 100 completed,
average wait 0.13 steps; 2.0x surge, 200 riders, 195 completed,
average wait 44.08 steps, 5 unserved riders.

### Greedy vs optimal assignment (`optimize.py`)
For a small fleet, brute-force optimal assignment is compared
with the greedy assignment above. Verified, 8 vehicles and
8 riders, seed 42: greedy total distance 22.73, optimal total
distance 17.50, a 29.87% greedy gap. That gap is why real
dispatch needs solvers and heuristics, and why greedy alone is
not claimed as optimal here.

## 2. Perception verification and validation (`perception_vv.py`)
Synthetic ground-truth objects and detector outputs with controlled
noise, matched by centre distance. Output: precision, recall, F1,
false positives, false negatives, failure rates by synthetic
condition (near, far, rain, occluded), and confidence calibration
by bin.

## Honest limits
- All data here is synthetic and generated with a fixed seed.
  This is not Zoox data, not a production dispatch system, and
  not a safety validation of any real perception system.
- The fleet assignment is greedy nearest-vehicle, not an
  optimization solver. It is a baseline to learn from, not a
  claim of optimal routing.

## Run
```
python3 verify.py
streamlit run streamlit_app.py
```
`verify.py` runs both demos with fixed seeds and checks that all
metrics stay in valid ranges. `requirements.txt` is streamlit only;
the core modules use the Python standard library.
