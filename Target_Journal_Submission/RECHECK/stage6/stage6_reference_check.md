# Stage 6.1 reference re-verification (2026-11-23)
Script: stage6/verify_refs.py -> stage6/reference_verification_v2.csv (90 BibTeX entries: 39 background + 51 novelty).
- 82/82 DOI entries: Crossref/DataCite title similarity >= 0.8, year and first author match, except two documented
  online-vs-print year differences (Beebe 2013 online 2012; Tautz-Weinert 2017 online 2016) -> keep print year.
- No-DOI entries verified on OpenAlex (title, year, venue, first author): Ke 2017 LightGBM (W2768348081, NeurIPS),
  Tatbul 2018 range PR (W2890573771, NeurIPS), Holm 1979 (W2121044470, Scand J Stat), Demsar 2006 (W1565746575, JMLR).
- ANSI/ISA-18.2-2016: existence and title verified on webstore.ansi.org (standard; content not read) -> cite only
  as "alarm-management lifecycle standard".
- EEMUA 191 (3rd ed. 2013): listed as withdrawn/superseded by a 2024 4th edition (IHS catalogue entry); neither
  edition could be read -> DROPPED.
- Content check ("does the paper say what we attribute"): done per claim in the claim-evidence table (Stage 6.2),
  using abstracts (full texts only where open). Citations whose support is title-only (Mansson 2019, Izadi 2009)
  are used only for the topic they name, never for a specific number.
