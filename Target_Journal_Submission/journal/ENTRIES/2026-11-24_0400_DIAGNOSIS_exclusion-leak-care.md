# DIAGNOSIS — the online trainer could "know" an anomaly before it was reported (written at the time)
While reading the CARE labelling code before its first run we saw that src/models/online.py treats an exclusion
interval as known once its start is more than 7 days in the past. For CARE, the pre-anomaly exclusion starts 14 days
before the event, so the trainer would drop pre-anomaly data up to a week before the anomaly starts, i.e. long before
it is reported (event_end). It also never removed past anomaly windows from training. This is the same family of
leak the RECHECK lineage found in 4/982 PreDist fits. We fixed it for CARE only (exclusions known only after
event_end; anomaly windows excluded after their report), leaving the PreDist path unchanged so committed PreDist
numbers stay reproducible; a PreDist sensitivity run with the fixed rule is planned.
