
## v0.20 - Target-zone wording and oak keystone wording
- Updated target-zone logic popup to say plants are treated as target-zone native when documented from at least three counties inside the mapped City of Kyle target-zone county bubble.
- Clarified that counties west, east, or south of Hays County can count when they are inside the mapped bubble, including West Texas and South Texas portions of the target zone.
- Removed public wording naming *Quercus virginiana* as the current 100-point benchmark.
- Added public wording describing oaks (*Quercus*) as keystone-style food-web plants with high documented animal interactions.

# Changelog

## v0.15 native-weighted scores
- Added native-status weighting to the balanced score.
- Kept ecological score unadjusted as the raw documented direct animal-use signal.
- Target-zone native plants receive a small boost.
- Non-native plants receive score reductions.
- Invasive/high-caution plants receive strong score reductions and remain do-not-recommend.
- Added score logic audit file: docs/score_logic_v0_15.csv.

# Changelog

## v0.14 target-zone thumbnails/layout
- Widened the dashboard layout and made the Open button sticky at the right edge of the table.
- Simplified target-zone status wording to public-facing text.
- Added a Target-zone logic modal with the City of Kyle target-zone map.
- Removed the visible “no current caution flag” chip from normal plant rows.
- Added iNaturalist plant thumbnails in the plant table and animal thumbnails in plant detail rows. Photos remain visual references only and are not scoring evidence.
- iNaturalist photo search strips variety/subspecies suffixes for better plant image matching.

# Changelog

## v0.8 public-clean
- Hid internal source-layer/workbook labels from the public interaction table.
- Replaced technical source wording with public citation wording.
- Removed public source inventory and filter-log tables from the dashboard.
- Kept citations, source statements, instructions, plant flags, and interaction details.
- Kept permanent dark mode and GitHub-safe external CSV loading.

## v0.10 - Balanced score recalibration

- Recalibrated host, pollinator, bird, mammal, other, evidence, locality, and overall scores.
- Reduced score saturation so fewer plants receive 100 in a category.
- Added score bands in the UI: none, low, modest, strong, top.
- Updated public wording to explain that low/blank scores often mean data are not yet complete.
- Kept internal build/source-layer wording out of the public interface.


## v0.11
- Expanded target-zone public grades from A-D/limited into A-F bands.
- Added a Score grade dropdown filter to separate plants by grade.
- Added public note explaining that low grades can mean limited verified direct-interaction data, not ecological worthlessness.


## v0.12 - Score breakdown and dual scores
- Added ecological score beside balanced score.
- Added click-to-expand score category explanations.
- Added grade basis filter for ecological vs balanced grades.
- Added score sort options for balanced and ecological score.


## v0.13 - Mammal handoff layer

- Imported `Import_Ready_No_Crops` from the final mammal dashboard handoff workbook.
- Added The Mammals of Texas as the primary mammal source statement and row-level citation family.
- Updated mammal score and dual ecological/balanced scores.
- Added mammal mapping audit and summary CSVs under `docs/`.

## v0.17 - Semi-release citation cleanup and soil layer

- Cleaned Hays/Central Texas insect citation display to hide raw CSV/source-layer text from public plant rows.
- Suppressed raw iNaturalist/photo URLs in interaction citations when they are not formal source citations.
- Added citation audit files for public source buckets.
- Added a separate Mammal Soil Engineers tab from the soil handoff workbook.
- Kept plant scoring unchanged from v0.16. Soil-engineering rows do not affect plant scores.


## v0.19 modal fix
- Fixed plant detail modal getting stuck on the loading message.
- Restored animal-group helper functions used by plant detail dropdowns.
- Added a safe balanced-score adjustment explanation block in plant details.
- Added defensive error handling so a single display issue does not leave the modal stuck.
