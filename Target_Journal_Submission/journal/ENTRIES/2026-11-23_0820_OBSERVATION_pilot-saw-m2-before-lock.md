RETROSPECTIVE entry reconstructed on 2026-11-24 from PROGRESS.md (commit 3c1504f) and code/experiments/TEST_LOCK.md 'Disclosure'; not written at the time.

# Pilot: control-loop deviations before fault reports

Exploratory pilot (code/experiments/pilot/pilot_signals.py): "44% of 54 faults show |z|>4 control-loop deviation in 7 d
before report vs own 120-d baseline". We had not yet measured the normal-day false-alarm rate.

The pilot printed per-fault z-scores for M1 AND M2 faults before the test lock was written. No detector, threshold or
model was fitted. TEST_LOCK.md discloses this. It is the first time we looked at M2 data.
