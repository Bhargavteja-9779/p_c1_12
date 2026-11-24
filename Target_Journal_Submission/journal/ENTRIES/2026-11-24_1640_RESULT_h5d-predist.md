# RESULT — the quiet-normal-period effect on district heating (written at the time)
On PreDist M1 the benchmark's 35 normal weeks raise alarms less often than random normal weeks of the same
substations: pooled ratio 0.47 (95% CI 0.20-0.73), so the pre-registered H5d holds. It is not uniform: the
rule-based detectors never alarm on any curated normal week (vs 3-5% of random weeks), but the two autoencoders
alarm on curated and random weeks equally often (ratios 1.0 and 1.07). We had to add the pooled CI after the first
run because the pre-registered script computed only the point estimate; nothing else changed (D-15).
An honest reading: the curated weeks avoid the kind of disturbance that loop-based rules react to; the AE's false
alarms are driven by seasonal regime changes (earlier mechanism analysis, results/mechanism_fa_ae.csv), which the
curation does not avoid. This is a hypothesis, not yet tested.
