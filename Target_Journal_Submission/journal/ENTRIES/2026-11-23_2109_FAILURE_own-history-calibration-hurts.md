RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md focused-wozniak 'F17 substation calibration' (commit 5f62f1f, 21:09); results/round5/; not written at the time.

# Substation-calibrated evidence makes things worse (focused-wozniak)

- H5a FALSIFIED: calibrated rule OR calibrated AE reaches "0.321 < 0.429".
- H5b FALSIFIED: the top-5 substations' FA share goes from "0.376 (C2) -> 0.470".

Stated diagnosis:
- calibrating against a substation's own past makes quiet substations alarm on deviations that are normal fleet-wide;
- it pushes faults in chronically poor substations below threshold;
- "Absolute, physically scaled evidence (Kelvin of shortfall) carries information that rank calibration discards."

The idea was dropped and kept as a negative result.
