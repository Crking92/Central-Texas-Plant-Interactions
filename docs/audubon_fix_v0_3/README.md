# Audubon bird layer repair v0.3-audubon-fix

This package keeps the National Audubon Society Native Plants data, but repairs how it is represented.

## Problem fixed

The previous dashboard represented Audubon rows as plant x split bird-label x resource direct-food rows. That created rows such as a grass supporting hummingbirds through nectar when the Audubon page was only providing broad May Attract / plant-resource profile information.

## New representation

Audubon records are retained as trusted broad profile support:

- `rank = broad_audubon_group`
- `category = Broad bird habitat/resource support`
- `use = Bird-friendly profile support`
- `evidence = D - Audubon broad bird-friendly support; not species-level direct interaction`
- `weight = 0.07`

Plant resources are not cross-multiplied by bird group. Species-level bird claims still come from AvianDiet/GloBI/LBJ profile rows where present.

## Row count change

- Old Audubon cross-product rows: 3,541
- New Audubon broad profile rows: 855
- Rows removed from public interaction detail noise: 2,686
- Total interaction rows loaded by dashboard after repair: 48,557

## Files changed

- `data/dashboard_interactions_v0_3.csv`
- `data/dashboard_interactions_v0_3_part1.csv`
- `data/dashboard_interactions_v0_3_part2.csv`
- `data/dashboard_interactions_v0_3_part3.csv`
- `data/dashboard_plants_v0_3.csv`
- `data/dashboard_sources_v0_3.csv`
- `index.html`

## Audit files

- `audubon_profile_row_collapse_summary.csv`
- `audubon_removed_crossproduct_rows.csv`
- `audubon_fixed_profile_rows.csv`
- `audubon_score_changes.csv`

## When a full re-scrape is still useful

A full Audubon re-scrape is only needed if you want exact current Audubon species-page resource labels and exact current bird-family labels for every plant. This repair is safe as a patch because it removes the false cross-product claim and keeps the Audubon data as broad trusted support.
