from pathlib import Path

import pandas as pd


# TODO : move config in .env file
DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "palworld_database",
}

RAW_DATA_DIR = Path(__file__).resolve().parent / "raw_data"

DATA_EXTRACTORS = {
        "combat-attribute": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data--Palu combat attribute table.csv", skiprows=1),
        "refresh-area": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data--Palu refresh level.csv", skiprows=4),
        "job-skill": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data-Palu Job Skills Table.csv", skiprows=1),
        "hiden-attribute": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data-hide Pallu attributes.csv"),
        "tower-boss-attribute": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data-Tower BOSS attribute comparison.csv", index_col="name").T,
        "ordinary-boss-attribute": lambda: pd.read_csv(RAW_DATA_DIR / "Palworld_Data-comparison of ordinary BOSS attributes.csv",  skiprows=3)
    }
