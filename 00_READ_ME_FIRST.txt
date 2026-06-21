GLASS ROOT GARDEN DASHBOARD — GITHUB WEB UPLOAD BATCHES
==========================================================

IMPORTANT
---------
Do not upload this whole package at once, and do not drag the numbered batch
folder itself into GitHub. Open each numbered folder and drag EVERYTHING INSIDE
it into the upload box at the ROOT of your GitHub repository.

BEFORE YOU UPLOAD
-----------------
The old bulk CSV files must be removed or they will remain publicly available.
Delete these old repository items first:

  data/
  docs/
  downloads/
  support/
  MANIFEST.csv

The new upload recreates the clean data folder. The new index.html and README.md
replace the old versions.

UPLOAD ORDER
------------
At the main/root page of the repository, choose Add file > Upload files.
Upload and commit one numbered batch at a time:

  1. 01_UPLOAD_FIRST_MAIN_FILES       12 files
  2. 02_UPLOAD_SECOND_DETAILS         90 files
  3. 03_UPLOAD_THIRD_DETAILS          90 files
  4. 04_UPLOAD_LAST_DETAILS           76 files

For every batch:
  1. Open the numbered folder on your computer.
  2. Select everything INSIDE it.
  3. Drag the selected files and folders into GitHub's upload box while you are
     at the ROOT of the repository.
  4. Wait for GitHub to list all files.
  5. Commit the upload before starting the next batch.

Because each batch contains the correct repository paths, GitHub will place the
files inside assets/, data/, and data/details/ automatically.

AFTER THE FOUR BATCHES
----------------------
Open the GitHub Pages dashboard and test:
  - Search for Quercus
  - Open a plant record
  - Open a second plant from a different example group
  - Confirm the Glass Root Garden watermark appears
  - Confirm the Rights and Citation links open

LIMIT CHECK
-----------
Every upload batch contains fewer than 100 files.
The largest individual upload file is dashboard_plants_v0_3.csv at about 7.46 MB,
well below the 25 MiB browser-upload limit.

The file BATCH_MANIFEST.csv lists every upload path, size, checksum, and batch.
