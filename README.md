# pals-analysis

## Problèmes rencontrés
- Noms des CSV mal formatés
- combat-attribute :
  - lvl1, lvl2, lvl3, lvl4, lvl5 pas les bons caractères


## TODO : 
- Mettre un lien pour télécharger les données dans Getting Started
- Scripts install.sh et run.sh
- etl.py

  - Faire une table pals
    - ID
    - English name
    - Chineise name
    - Volume size (Size)
    - Tribe
    - GenusCategory
    - Price ?

  - hidden-attribute :
    - BPClass et Tribe meme chose ?


## Getting started
- Create MySQL Database named `palword_database` (or change database in config)
- Migrate raw data in database :
```shell
# Run pipeline
python etl.py
```