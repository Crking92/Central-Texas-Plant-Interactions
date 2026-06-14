# Provenance note — insect data collection chat

User-provided chat-history notes indicate that the insect dashboard was built from a sifted version of a global interaction download and later given a blanket GloBI citation section.

Verified file evidence in the current dashboard package supports this interpretation:

- `dashboard_sources_v0_3.csv` lists `Hays-County-Insect-Interactions-main.zip / central_texas_insect_interactions_simplified.csv` as a regional insect source layer.
- `dashboard_sources_v0_3.csv` also lists `central_texas_interactions(7).xlsx / GloBI raw` as a raw GloBI-style interaction source.
- The uploaded `central_texas_interactions(8).xlsx` has the structure of a GloBI-style interaction table.
- `dashboard_interactions_v0_3.csv` contains 3,620 rows mentioning `Hays County Insect simplified.csv`, including 2,045 rows where it is the only listed source layer.

Recommended public wording:

> This insect layer is a filtered/processed derivative of Central Texas plant-insect interaction records assembled from GloBI-style interaction data and row-level contributor records. GloBI / Poelen et al. 2014 is cited as blanket provenance; row-level citations are retained when present.

Blanket citation:

Poelen, J.H., Simons, J.D., & Mungall, C.J. 2014. Global Biotic Interactions: An open infrastructure to share and analyze species-interaction datasets. Ecological Informatics 24:148-159. https://doi.org/10.1016/j.ecoinf.2014.08.005
