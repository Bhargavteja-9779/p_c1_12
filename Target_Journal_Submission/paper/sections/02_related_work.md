<!-- DRAFT cycle 4. Sources: literature/claim_table.md, literature/prior_art_cycle4.json (opened=true only).
     Citation keys are DOIs until the bibliography is assembled. Unreviewed items are marked as such in the text. -->

## 2. Related work

We organise prior work by the gap this paper addresses: what an operator learns from a published evaluation about
the alarm load of a detector in continuous operation.

### 2.1 Why balanced test sets overstate precision

That precision depends on prevalence is old knowledge. Axelsson showed for intrusion detection that a detector with
a low false-positive rate still produces mostly false alarms when attacks are rare [10.1145/319709.319710;
10.1145/357830.357849], and the same base-rate argument underlies the advice to read precision–recall results at
the prevalence of the deployment setting [10.1371/journal.pone.0118432] and recent low-prevalence evaluations in
medical imaging [10.48550/arxiv.2604.11171]. The authors of the PreDist district-heating dataset state the effect
for their own benchmark: their reliability score uses a balanced set of fault and normal windows, and they note that
precision is likely lower under realistic class imbalance but keep a 50/50 split because no canonical ratio exists
[10.1016/j.energy.2026.141178]. The CARE to Compare wind benchmark uses the same design: its reliability term is an
event-wise F0.5 over roughly equal numbers of anomaly and normal datasets, with an alarm declared when a criticality
counter reaches 72 ten-minute steps [10.3390/data9120138]. We therefore do not claim the mechanism. What has been
missing is its size on these benchmarks: nobody had replayed the detectors over the full continuous history of the
PreDist and CARE assets and compared event precision with the alarm precision an operator would experience.

### 2.2 Evaluation protocols that change conclusions

In time-series anomaly detection, Kim et al. showed that the point-adjust protocol inflates scores enough to
produce misguided rankings [10.1609/aaai.v36i7.20680]; other work proposed evaluation frameworks for temporal
unsupervised detection in predictive maintenance [10.1016/j.neucom.2021.07.095] and showed that calibrating
thresholds on the test set biases results [10.5220/0014392600004084]. Salem and Ferrugem report that a
low-false-alarm evaluation changes the ranking of multisensor anomaly detectors [10.55972/spectrum.v27i1.439].
In wind energy, a leakage-controlled evaluation on CARE (preprint, [10.5194/wes-2026-145]) and a cross-asset
conformal protocol [10.3390/info17090930] both find that calibrating thresholds on the evaluated assets gives
optimistic thresholds and many false alarms. These studies establish that protocol choice matters. They do not
separate how much of a ranking change comes from tuning thresholds on the evaluated events and how much from the
event-window design itself, and none covers district heating. Our protocol comparison isolates these two factors
(Section 6.2).

### 2.3 False-alarm budgets and how many normal periods a test needs

False-alarm rates per unit of operating time are the standard acceptance criterion in fields with mature alarm
practice, and the statistics of certifying such a rate with a finite test are worked out, e.g. binomial and Poisson
designs for radiation portal monitors [10.6028/nist.tn.2118] and for mine detection [10.2172/1032]. Wind-energy
benchmarks have begun to report false-alarm hours per year [10.5281/zenodo.24164281, unreviewed software release].
We apply this standard statistics to the event-window design of PreDist and CARE as a design check (Section 6.4);
the calculation itself is not a contribution.

### 2.4 Transfer across fleets

Transfer of normal-behaviour models between wind turbines has been studied with autoencoders
[10.1016/j.egyai.2024.100373], and a pooled CARE model was reported unable to hold a stable operating point across
farms [10.1109/ubmk71847.2026.11745258]. For district heating, van Dreven et al. proposed a substation-invariant
self-supervised transformer and tested it on PreDist with both control-unit manufacturers, including M1-to-M2
transfer [10.1016/j.egyai.2026.100824]; they score daily windows of which 20-83% of samples are faulty and report
F1 at the best threshold, without a false-alarm rate over time. Closest to our CARE analysis, a blinded, pre-registered study of public
wind SCADA data (manuscript under review; reproducibility package [10.5281/zenodo.23902232]) reports detection
without discrimination at alarm budgets, a random-alarm reference and cross-farm threshold transfer. We regard it as
concurrent, independent evidence for the wind part of our results. For district heating, cross-manufacturer transfer on PreDist has
therefore been studied [10.1016/j.egyai.2026.100824], but with thresholds chosen at their best value on the evaluated
windows; no study has locked thresholds on one manufacturer at a false-alarm budget, applied them unchanged to the
other in continuous operation, or compared every operating point with random alarms raised at the same rate.

### 2.5 Summary of the gap

| Claim in this paper | Closest prior work | Exact difference |
|---|---|---|
| Event precision exceeds deployed alarm precision by a large factor | PreDist paper (qualitative); Axelsson (mechanism) | We measure the factor per detector on both public energy benchmarks by replaying all detectors over continuous operation. |
| Benchmark-chosen thresholds give many false alarms per asset-year | Leakage-controlled CARE studies (wind) | We convert the thresholds selected by the PreDist/CARE event protocols themselves into false alarms per asset-year. |
| Rankings change between protocols, mostly through threshold tuning on evaluated events | Kim et al.; Salem and Ferrugem | We decompose the change into threshold tuning and window design, on two energy benchmarks. |
| Event protocols cannot resolve operational false-alarm rates | NIST TN 2118 (method) | Applied to the PreDist/CARE designs (supporting check only). |
| Budgeted thresholds do not transfer across control-unit manufacturers (district heating) | van Dreven et al. 2026 (PreDist M1-M2, best-threshold F1); Song (concurrent, wind) | Thresholds locked at a false-alarm budget on one manufacturer and applied unchanged in continuous operation, with a matched-rate random-alarm reference. |
