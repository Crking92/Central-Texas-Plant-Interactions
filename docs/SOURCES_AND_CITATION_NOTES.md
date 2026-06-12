# Sources and citation notes

This dashboard is a compiled, staging-level synthesis. The row-level CSV and workbook outputs are the audit trail.

## Major source families

- User-supplied target-zone plant master list
- Texas Host Plants / UDELep / host-calculator records
- Central Texas bee evidence rows
- Hays County insect interaction rows
- Central Texas bird/Audubon data
- Central Texas Bird Data Transfer Package, especially Bird_Master, Bird_Diet_AvianDiet, GloBI_BirdPlant, BIRDBASE, NestTrait, Plant_Resource_To_Validate, and Evidence_Rules
- LBJ Wildflower Center plant profile wildlife-use fields where available
- Central Texas mammal interaction data, heavily filtered for direct plant use
- GloBI-style raw interaction data, direct animal-plant rows only
- TexasNonNatives.org non-native crosswalk
- TexasInvasives / TDA / City of Austin invasive caution screens

## Evidence handling

- Species-level direct plant use has the highest scoring value.
- Genus/family/guild-level records are shown but down-weighted.
- Bird Master tables are used for bird identity/context.
- Avian Diet and GloBI bird-plant tables are retained as plant-use evidence tables.
- BIRDBASE and NestTrait provide bird context only and are not treated as plant-specific proof by themselves.
- Plant_Resource_To_Validate gates plant recommendations.
- A-E evidence rules are carried forward from the uploaded workbook.

## Public communication note

Recommended wording: "These are source-backed records in this build, not the complete universe of wildlife interactions. Missing records usually mean the interaction has not yet been added or validated."


## v0.6 Host Calculator source mappings

- **UDELep / Lepidoptera**: Shropshire, K. J. & Tallamy, D. W. 2025. *Lepidoptera of North America, north of Mexico: an annotated list containing geographic ranges and host-plant records.* ZooKeys 1261:101-113. DOI: https://doi.org/10.3897/zookeys.1261.160796
- **Sawflies**: Sawfly GenUS, USDA/APHIS PPQ IDtools: https://idtools.org/sawfly/index.cfm
- **Bark and ambrosia beetles**: T. H. Atkinson, Bark and ambrosia beetles of the Americas: https://barkbeetles.info/americas_index.php
- **Bee host/pollen data**: Fowler, J. 2020. Pollen Specialist Bees of the Central United States: https://jarrodfowler.com/bees_pollen.html
- **Gall makers**: Gallformers.org plant gall database: https://www.gallformers.org/

Rows from `central_texas_host_identifier_fixed.xlsx` still need a citation-recovery pass because the dashboard export preserved the workbook/table source but not the original reference.


## Central Texas Host Identifier / GloBI

Central Texas Host Identifier rows were created from GloBI-derived species interaction records. Use this blanket source statement for the current dashboard layer: Global Biotic Interactions (GloBI), with the formal citation Poelen, J. H., Simons, J. D., & Mungall, C. J. 2014. Global Biotic Interactions: An open infrastructure to share and analyze species-interaction datasets. Ecological Informatics 24:148-159. DOI: 10.1016/j.ecoinf.2014.08.005.

GloBI notes that derivative work should also cite original indexed data contributors when those row-level dataset citations are available. The dashboard keeps the blanket GloBI citation for Central Texas Host Identifier rows because the older workbook export was the preserved source layer.
