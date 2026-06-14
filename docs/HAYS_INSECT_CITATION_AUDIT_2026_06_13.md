# Hays insect citation audit — 2026-06-13

## Question checked

Do the roughly 2,000 insect rows from `Hays County Insect simplified.csv` have usable citation support, and what is still missing?

## Result

The audit found **2,045 dashboard rows** where `Hays County Insect simplified.csv` is the only listed source layer. These rows should be kept, but the dashboard should make the source trail clearer.

| Bucket | Meaning | Rows |
|---|---|---:|
| Clickable iNaturalist observation | Direct iNaturalist observation URL parsed | 1,835 |
| Clickable specimen/network URL | Ecdysis, SCAN-Bugs, AMNH-style, or similar specimen/network URL parsed | 119 |
| UUID record ID, no clickable URL | Recoverable digital identifier but no URL parsed | 83 |
| Named database/catalog, no clickable URL | Source clue exists, but manual recovery needed | 8 |

## Dashboard-wide insect citation gap check

| Check | Rows |
|---|---:|
| All dashboard insect rows | 46,741 |
| Missing source label | 0 |
| Missing citation text | 0 |
| Without clickable URL | 91 |
| Without URL / DOI / UUID | 8 |

The no-click and no-digital gaps are confined to the Hays-only source set in this extraction.

## Recommended GitHub wording

The insect layer was built from a filtered Central Texas plant-insect interaction workflow using GloBI-style interaction data and row-level contributor records. `Hays County Insect simplified.csv` is treated as a processed source layer. GloBI / Poelen et al. 2014 is used as a blanket provenance citation, while row-level citation text and URLs are retained in `hays_insect_citations_2045.csv`.

## Files

- `data/hays_insect_citations_2045.csv` — row-level evidence table for the 2,045 Hays-only rows.
- `data/hays_insect_manual_recovery_needed_91.csv` — no clickable URL parsed.
- `data/hays_insect_no_digital_locator_8.csv` — highest-priority manual recovery rows.
- `docs/all_insect_citation_gap_check.csv` — confirms no broader insect citation-text gap was detected.

