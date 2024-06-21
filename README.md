# pals-analysis

## Problèmes rencontrés
- Noms des CSV mal formatés
- combat-attribute :
  - lvl1, lvl2, lvl3, lvl4, lvl5 pas les bons caractères


## TODO
- Mettre un lien pour télécharger les données dans Getting Started
- Scripts install.sh et run.sh

- PIPELINE
  - connecter les tables et suprimer les colonnes redondantes
    - hidden-attribute
    - tower-boss-attribute
    - ordinary-boss-attribute


## Getting started
### Install
#### Install dependencies
- Open git bash
- You can create a virtual environment and activate it :
  ```shell
  # Create virtual environment
  python3 -m venv venv  # For Linux / Mac
  python -m venv venv  # For Windows

  # Activate virtual environment
  source venv/bin/activate  # For Linux / Mac
  source venv/Scripts/activate  # For Winwdow
  ```

- Install dependencies :
  ```shell
  pip install -r requirements.txt
  ```

#### Download dataset
- Go to [Google Drive folder URL](https://drive.google.com/drive/folders/1dTodDVBh_lwzmeuM-FB9P9RdsuAxdMgu?usp=drive_link)
- Download folder
- TODO : ajouter capture d'écran ?
- Unzip in project root AND DONT CHANGE FILE NAMES ! (if you want to change it you have to change in config)
- Create MySQL Database named `palword_database`
- Change DB_CONFIG in src/config.py with your username, password, and host

#### Process Pipeline
- Run process_pipeline script :
  ```shell
  python src/process_pipeline.py
  ```

### Use
- ... ?