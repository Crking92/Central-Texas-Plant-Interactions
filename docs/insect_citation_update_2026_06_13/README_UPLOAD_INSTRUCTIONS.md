# Hays County insect citation patch

Prepared for the Central Texas Plant Interactions dashboard.

## What this patch does

This patch adds row-level citation support for the **2,045 insect interaction rows** where the only listed source is `Hays County Insect simplified.csv`.

It does **not** replace the whole dashboard. It is a small GitHub overlay/companion package.

## Main files to upload/commit

- `data/hays_insect_citations_2045.csv`  
  Row-level citation table for the 2,045 Hays-only insect rows.

- `data/hays_insect_manual_recovery_needed_91.csv`  
  Rows that have citation text but no clickable URL parsed. Most still have UUID/specimen/catalog clues.

- `data/hays_insect_no_digital_locator_8.csv`  
  Highest-priority manual recovery rows. These have no URL, DOI, or UUID parsed by the audit.

- `data/dashboard_sources_v0_3.csv`  
  Replacement/updated source inventory with a clearer Hays insect source note.

- `docs/HAYS_INSECT_CITATION_AUDIT_2026_06_13.md`  
  Human-readable audit summary.

## Citation status

| Check | Rows |
|---|---:|
| Hays-only insect rows | 2,045 |
| With clickable row-level source URL | 1,954 |
| Without clickable URL | 91 |
| With UUID/specimen ID but no clickable URL | 83 |
| No URL / DOI / UUID parsed | 8 |

## Blanket provenance citation

Use this as the broad dataset/provenance citation for the GloBI-derived workflow:

Poelen, J.H., Simons, J.D., & Mungall, C.J. 2014. Global Biotic Interactions: An open infrastructure to share and analyze species-interaction datasets. *Ecological Informatics* 24:148-159. https://doi.org/10.1016/j.ecoinf.2014.08.005

Important: the blanket GloBI citation should explain the source pipeline. It should **not** replace row-level citations when row-level iNaturalist, specimen, DOI, or contributor citations are present.

## Remaining source risk

No Hays-only row is missing citation text in the extracted dashboard layer. The remaining issue is link recoverability:

- **91 rows** need clickable URL recovery if you want every row to open a source directly.
- **8 rows** are highest priority because no URL, DOI, or UUID was parsed.

