<!-- DRAFT cycle 4. Numbers from code/results/round6/care_dataset_facts.csv. -->

### 3.x Replication dataset: CARE to Compare (wind turbines)

To test whether the protocol gap is specific to district heating we use CARE to Compare [10.3390/data9120138],
a public benchmark of 10-minute SCADA data from three anonymised wind farms (Zenodo record 14958989, CC BY 4.0).
The benchmark ships 95 datasets: 45 that end in a labelled anomaly event and 50 normal events. Each dataset is a
slice of one turbine's history, and slices of the same turbine overlap; where they overlap the values are identical
(maximum absolute difference 0.0), so we merge all slices of a turbine into one continuous series. This gives 36
turbines and 48.9 turbine-years of data: farm A 5 turbines (83 columns, 8.2 turbine-years, 12 anomaly and 10 normal
events), farm B 9 turbines (254 columns, 10.7 turbine-years, 6 and 9 events) and farm C 22 turbines (954 columns,
30.1 turbine-years, 27 and 31 events). Normal events last 13.5 to 21.3 days on average per farm, longer than the
7-day normal weeks of PreDist.

The farms are anonymised; whether they use turbines from different manufacturers is not stated, so we speak of
cross-farm rather than cross-manufacturer transfer. No detector output on CARE was computed or inspected before the
analysis plan, the confirmation seeds and the analysis script were fixed (pre-registration and amendment A1 in the
project log, commit history of `code/scripts/round6_care.py`).

Continuous protocol on CARE. We use the same code path as for PreDist: 30-day burn-in; each turbine's detector is
retrained every 90 days on up to 730 days of its own past, using only rows with status code 0 (normal operation, the
CARE convention) outside exclusion intervals that are known at training time. An anomaly event's detection window
is [event start, event end); the exclusion intervals are the 14 days before the window, the window itself (for later
training) and the 2 days after it, and all of them become known to the trainer only at the event end. Alarms are
counted with the same criticality counter, a 24-hour refractory period and false alarms per turbine-year.
Operating points are chosen leave-one-farm-out: for each farm, the (threshold, counter) pair with the highest
recall within the false-alarm budget on the two other farms is applied unchanged to it.
