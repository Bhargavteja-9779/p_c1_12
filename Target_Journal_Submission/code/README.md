# Continuous-monitoring evaluation of fault detectors for district heating substations (PreDist)

Code for the manuscript submitted to *Energy and AI*. Code is available from the corresponding author on request.

## Data
PreDist (Fraunhofer IEE / enercity), Zenodo record 19496480, CC-BY-4.0: 93 substations, two manufacturers.
`scripts/download_data.sh` fetches it into `data/raw/`; `scripts/build_cache.py` builds `data/cache/`.
Manufacturer 1 (35 substations) is development data; manufacturer 2 (58 substations) is the locked test
set (`experiments/TEST_LOCK.md`), evaluated once with thresholds chosen on manufacturer 1.

## Install and run
```
pip install -r requirements.txt   # torch: --index-url https://download.pytorch.org/whl/cpu
python3 run_all.py --mode quick   # fast methods, seed 0
python3 run_all.py --mode full    # all cells, seeds 0-9, locked evaluation
python3 -m pytest -q tests
```

## Layout
- `src/data` PreDist loader; `src/features` control-loop extraction (measurement, setpoint pairs)
- `src/models` baselines (rule, 3-sigma, isolation forest, own quantile NBM, AE variants), SRCR fleet
  quantile model, online retraining runner and criticality counter
- `src/evaluation` continuous-monitoring protocol (every 10-min step, false alarms per substation-year,
  recall at fixed false-alarm budgets), threshold-free fault ranks
- `scripts` one script per experiment; `experiments/protocol.md` pre-registration and dated amendments;
  `experiments/novelty_escalation_log.md` every idea tried, with results (including failures)
- `results/` CSV outputs (score files are regenerated, not stored)
