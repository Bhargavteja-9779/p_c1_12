# Stage 3 close calls, verified by the main agent from primary records (2026-11-23)

| Paper | Verified how | Overlap | Our honest position |
|---|---|---|---|
| PreDist paper (Energy 2026, 10.1016/j.energy.2026.141178; arXiv 2511.14791) | full text of arXiv version read | same data, same task; its AE is one of our 11 cells; it concedes its balanced protocol overestimates reliability | we quantify that overestimate and replace the protocol; we never claim to be first on PreDist |
| Bahronov 2026, LUT thesis (OpenAlex W7162615597) | OpenAlex abstract | uses PreDist; regression/tree residual + Shewhart charts; compares false alarms with a threshold method | cite; drop any "first to consider false alarms on PreDist" claim; difference: no budgeted continuous protocol, no locked cross-manufacturer test, no chance reference |
| Salem & Ferrugem 2026, Spectrum (10.55972/spectrum.v27i1.439) | Crossref abstract | shows low-false-alarm evaluation changes detector rankings on 4 public multisensor datasets (not energy) | cite as general evidence; our claim is restricted to DH substations and to transfer across controller manufacturers |
| From lab to practice, Energy and AI 2026 (10.1016/j.egyai.2026.100824) | agent: OpenAlex reference list includes PreDist Zenodo v1 | DH transfer across networks, asymmetric | cite; we do not claim to be the first DH transfer study |
| Threshold transfer & metric inflation in ICS (10.5281/zenodo.23471990, code record only) | agent | thresholds fail across plant releases | cite only as a code record (article not found) or omit |

## Claims dropped or narrowed (applied to manuscript)
- "first to show rankings change at low false-alarm budgets" -> DROPPED (general); kept only "in DH, across manufacturers".
- "first locked/frozen protocol in condition monitoring" -> narrowed to DH substations (CARE-based wind papers use frozen protocols).
- "new seasonal mechanism" -> "empirical attribution on labelled DH faults".
- "first factorial" -> "scope x representation x model-class factorial in DH" (wind has representation x detector).
## Claims that stand (no counter-example found in 135 papers)
- DH: recall at fixed false alarms per substation-year in continuous scoring; pre-registered locked cross-manufacturer test;
  comparison with random alarms at matched rate; certification bound for balanced benchmarks; start-up artefact.
## External dataset
No second public labelled DH-substation fault dataset exists (agent search). External validation of fault recall is
therefore impossible; unlabelled DH data could only measure alarm burden (not pursued: no labels, different signals).
