# Test-set lock (written 2026-11-23, before any detector was run on PreDist)

- DEVELOPMENT data: Manufacturer 1 (M1) only. All idea selection, hyperparameter tuning, threshold calibration
  and the novelty-escalation loop use M1 (with internal leave-substation-out / chronological splits).
- LOCKED TEST data: Manufacturer 2 (M2). No detector output on M2 is computed or inspected until the final
  candidate set is frozen in experiments/protocol.md. Each final candidate is evaluated on M2 exactly once.
- Disclosure: an exploratory pilot (experiments/pilot/pilot_signals.py) printed per-fault z-scores of five
  simple control-loop signals for M1 AND M2 faults before this lock. No detector, threshold or model was
  fitted; the pilot is reported as such.
- Any later access to M2 results is logged in experiments/novelty_escalation_log.md with date and reason.
