# RESULT — plan_v2 PreDist M1 seed 0 (pre-registered)
Ranking agreement with the deployment-like reference (out-of-sample thresholds, continuous replay):
balanced event windows + test-tuned thresholds tau 0.18; fixing thresholds alone 0.63; continuous replay alone 0.83.
H7a p 0.0045, H7b p 0.0215 (one-sided, before Holm; Holm across datasets after CARE). H7d supported (ratio 0.30).
Recall falls from 0.69-0.84 (event benchmark) to 0.04-0.29 (deployment-like) for all 17 detectors.
Next: CARE seed 0 inputs (temp3s, ae, ae_cond + panel care seed 0), then plan_v2_analysis.py care 0, then summary.
