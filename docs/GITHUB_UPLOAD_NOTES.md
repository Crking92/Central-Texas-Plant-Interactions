# GitHub upload notes

GitHub web upload rejects individual files larger than 25 MB. This package is GitHub-safe: no individual file is over 25 MB.

Upload the package contents to the repository root:

- `index.html`
- `assets/`
- `data/`
- `docs/`
- `downloads/`
- `support/`
- `README.md`

Important: do **not** upload `data/dashboard_interactions_v0_3.csv`. That single combined file was removed because it was over GitHub's web-upload limit.

The dashboard now loads the split interaction files instead:

- `data/dashboard_interactions_v0_3_part1.csv`
- `data/dashboard_interactions_v0_3_part2.csv`
- `data/dashboard_interactions_v0_3_part3.csv`

The current `index.html` already points to those three split files, so the large combined CSV is not needed.

## v0.3 Audubon fix

This version keeps Audubon as a trusted broad bird-habitat support source, but removes the incorrect cross-product rows that multiplied bird groups by fruit/seed/nectar resources.
