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

### Grade band adjustment

- Changed overall letter grades to use current-dataset bands rather than school-style bands: A >= 72, B >= 58, C >= 42, D >= 28, Limited below 28.
- This creates a more useful spread while the dataset is still growing.
