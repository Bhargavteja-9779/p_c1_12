# Energy and AI: style notes

These notes paraphrase what I observed in 40 sampled 2024-2026 research articles. Titles cover all 40. Abstracts come from OpenAlex for all 40. Body text comes from the 16 arXiv versions read in full; 4 of those are the Elsevier-typeset PDFs (100538, 100586, 100726, 100884). Anything I could not see is marked **NOT OBSERVED**.

## Titles

- **Length.** Mean title length is **13.35 words** (median 13, range 7-20, n = 40). Across all 596 non-review 2024-2026 titles in OpenAlex for the journal the mean is 13.8 words, so titles run fairly long.
- **Basic pattern.** The usual form is *[method or approach] for [task] in/of [energy asset or setting]*.
  - 28/40 titles contain "for".
  - "with" appears in 6, "using" in 3, "framework" in 6.
  - The word "novel" does not appear in any sampled title.
- **Two-part titles.** 11/40 (28%) use a colon, the same rate as across the journal (28%). Common forms:
  - an acronym followed by a description of the method (3/40, e.g. a coined model name such as HEAT, TRACE, EGBAD);
  - a short claim followed by its scope ("Concept drift detection in district heating: A characterization framework and ...").
- **Named settings.** The application setting is almost always named explicitly (wind turbines, district heating substations, PV plants, VRF systems, heat pumps).
- **Method family.** 13/40 titles name an ML family outright (deep learning, neural network, reinforcement learning, transformer, LLM).
- **Evidence words.** Some titles flag the kind of evidence ("Experimental validation of ...", "Real-world validation of ...", "Systematic evaluation of ...", "An empirical benchmark of ...").

## Abstracts

- **Length.** Single paragraph, unstructured (no headings). Median about **230 words** in the sample (mean 221, range 100-365). The journal-wide median over 622 abstracts is 221 words.
- **Typical order:**
  1. one or two sentences on why the energy problem matters;
  2. a sentence naming a gap or limitation of existing methods;
  3. "This paper/study proposes ..." or "We introduce/present ..." (37/40 abstracts contain such a phrase);
  4. a compact description of the method steps, often enumerated as "First, ... Second, ... Finally, ...";
  5. the data or experimental setting;
  6. headline quantitative results;
  7. a closing sentence on practical value.
- **Numbers in the results.** 27/40 abstracts give percentages, for example F1, error reductions or precision. Many also give absolute metrics.
- **Opening sentence.** Most abstracts (35/40) open with context or motivation rather than with "This paper".

## How introductions open

All 16 full texts open with a broad energy-transition or sector-importance statement, often with a statistic and citation. Examples:

- buildings' share of global energy use;
- the role of wind energy;
- the climate urgency driving renewables;
- the importance of district heating for decarbonisation.

The introduction then narrows quickly to the specific asset and the operational pain point: downtime, data scarcity, label scarcity, or lack of real-world validation. This is followed by a literature paragraph or a separate **Related work** section (present as a titled section or subsection in 11 of the 16 full texts), an explicit gap statement, the contributions, and often a closing "the remainder of the paper is organized as follows" roadmap paragraph.

## How contributions are listed

- **Format.** An explicit contribution list is typical, introduced by phrases such as "The main contributions of this paper are as follows" or "This study makes three contributions". It is seen in at least 11 of the 16 full texts. Format varies:
  - bullets (e.g. 100942, 100704, 100448, 100870, 100867, 100586);
  - numbered lists 1-4 (100538, 100726, 100884);
  - roman numerals (100626, 100933).
- **Placement.** Sometimes the list sits under its own subheading (e.g. "1.1 Contribution and outline", "1.2 Contributions", "1.3 Objectives and Contribution", or a separate "Scope and Contributions" section).
- **Number of items.** Usually 3-4 items. Each item starts with a verb or a noun phrase: proposed or designed method, evaluation or benchmark, insight or analysis, and sometimes open-source release.

## Sentence style

- **Voice.** First-person plural ("we propose", "we evaluate") is used freely and mixed with passive constructions in the method sections.
- **Terminology.** Domain-specific terms are spelled out once with an acronym and the acronym is used heavily afterwards (NBM, SCADA, DHN, TSFM, FDD, SOH, RLP). Several full texts carry a **Nomenclature** or abbreviation list (seen in 100373 and 100448).
- **Equations.** Equations are numbered. Metric definitions (MAE, RMSE, F1, CRPS etc.) are usually written out even when standard.
- **Claim strength.** Claims are fairly assertive in abstracts and highlights ("significantly", "consistently outperforms"). Bodies tend to be more hedged.
- **Typical paper type.** Method + case study. Results sections usually combine quantitative tables with qualitative case plots, such as an anomaly score over time before a documented failure.

## How limitations are stated

- **Dedicated subsection.** A titled limitations subsection is a minority: seen in 3/16 full texts, as "Limitations" under the discussion (100942, 100933, 100867).
- **Inline limitations.** More commonly limitations appear as a few sentences in the discussion or conclusion and lead straight into **future work**. Examples:
  - only one cell chemistry, so cross-cell generalisation is left for future work;
  - long training time is acceptable for the use case;
  - rare events remain hard to predict;
  - further research is needed on turbine-specific variation.
- **Tone.** Limitations are usually framed constructively and kept short. Threats-to-validity style sections were **NOT OBSERVED**.

## Section names and order seen in full texts

The most common skeleton is:

1. Introduction (with contribution list, sometimes as subsections)
2. Related work, or a literature subsection
3. Methodology / Method / Proposed model
4. Data / Dataset / Experimental setup (sometimes inside the method section)
5. Results and discussion (combined heading in 5/16), or Results followed by Discussion (separate Discussion in 7/16)
6. Conclusion(s)
7. Back matter:
   - CRediT authorship contribution statement (11/16);
   - Declaration of competing interest (9/16);
   - Data availability or Code & data availability (9/16);
   - Declaration of generative AI / AI-assisted technologies (seen in several 2025-2026 papers, e.g. 100726, 100867, 100942);
   - Acknowledgements;
   - References;
   - Appendices (common in preprints; long appendices with extra tables in benchmark papers).

Variants seen:

- Nature-style unnumbered "Results and discussion" with Methods after the results (100542).
- A theory section before the experiments (100538).
- A hybrid IMRaD/CRISP-DM structure stated explicitly (100867).

Numbered decimal headings (1., 1.1., 2.1.) are standard.

## Highlights and graphical abstract

- **Highlights.** Visible in 7/16 arXiv versions: all 4 typeset PDFs plus 100448, 100685, 100704, and 100870 (highlights only).
  - Usually 3-5 bullets of 10-20 words each.
  - They mix method statements ("A ranking-based SSL framework is proposed ...") with quantified results ("18.8% and 27.6% RMSE reductions vs baseline").
- **Graphical abstract.** Visible in 6/16 (the 4 typeset PDFs plus 100448, 100685, 100704). Content is a pipeline or overview diagram of the method. Image content was not inspected beyond the extracted text.
- **Authors' preprints.** The remaining preprints omit both items, so whether these are mandatory **could not be confirmed** from the sources I could access. The author guidelines on elsevier.com are blocked; **NOT OBSERVED**.

## Reference style hints

- **Numeric style.** Numbered citations in square brackets, with ranges allowed ([1-4], [44-48]), in 14/16 full texts and in all 4 typeset versions.
- **Typeset reference list.** Entries look like "[1] Surname AB, Surname CD, ... Title. Journal Year;Vol:pages. http://dx.doi.org/..." This is Elsevier's numbered Vancouver-like style with abbreviated first names, no full stops in initials, and DOIs given as links.
- **Exceptions in preprints.** One preprint uses author-year (Harvard) citations (100658). Another uses superscript numerals (100942). These are presumably converted during production; the final format is **NOT OBSERVED**.
- **Number of references.** Median 49.5 (range 22-100, Crossref, n=40). Self-citation to the group's earlier work and citations of Energy and AI and Applied Energy papers are common.
- **Keywords.** A keywords list (about 4-8 terms) appears in all 16 full texts.

## Not observable with available sources

- Official word or page limits.
- Required highlight character limits.
- The required graphical-abstract format.
- Mandatory statements.
- Submission template rules.

These would need the Guide for Authors on elsevier.com, which is blocked in this environment.
