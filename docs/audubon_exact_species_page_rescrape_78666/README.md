# Audubon exact species-page merge and insect citation update

Built for the GitHub dashboard package.

## Audubon correction

This version replaces the earlier uniform Audubon broad-guild patch with exact Audubon species-page results for ZIP 78666.

- Removed old uniform Audubon rows: 855
- Added exact Audubon bird-family support rows: 808
- Exact Audubon species profiles scraped: 72
- Audubon-only review plants added because they were not already exact matches in the dashboard plant table: 3

Audubon rows remain trusted broad plant-profile support. They are not species-level direct food-web claims, and plant resources are not multiplied into each bird-family group.

## Insect citation update

Merged the Hays insect citation patch into the GitHub package:

- `data/hays_insect_citations_2045.csv`
- `data/hays_insect_manual_recovery_needed_91.csv`
- `data/hays_insect_no_digital_locator_8.csv`
- citation audit summaries in `docs/insect_citation_update_2026_06_13/`

## GitHub-safe packaging

The combined dashboard interaction table is intentionally not included as one giant CSV. The dashboard loads the split files:

- `data/dashboard_interactions_v0_3_part1.csv`
- `data/dashboard_interactions_v0_3_part2.csv`
- `data/dashboard_interactions_v0_3_part3.csv`

No individual file in this package should exceed 25 MB.
