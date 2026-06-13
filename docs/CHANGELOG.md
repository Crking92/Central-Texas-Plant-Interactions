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
