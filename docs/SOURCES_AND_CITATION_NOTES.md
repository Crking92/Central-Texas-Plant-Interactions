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
