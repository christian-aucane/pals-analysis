from pathlib import Path
import logging

# TODO : move db config in .env and read it
DB_CONFIG = {
    "user": "root",
    "password": "leo",
    "host": "localhost",
    "database": "palworld_database",
}


RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "raw_data"

CSV_PATHS = {
    "combat-attribute": RAW_DATA_DIR / "Palworld_Data--Palu combat attribute table.csv",
    "refresh-area": RAW_DATA_DIR / "Palworld_Data--Palu refresh level.csv",
    "job-skill": RAW_DATA_DIR / "Palworld_Data-Palu Job Skills Table.csv", 
    "hidden-attribute": RAW_DATA_DIR / "Palworld_Data-hide Pallu attributes.csv",
    "tower-boss-attribute": RAW_DATA_DIR / "Palworld_Data-Tower BOSS attribute comparison.csv",
    "ordinary-boss-attribute": RAW_DATA_DIR / "Palworld_Data-comparison of ordinary BOSS attributes.csv",
}

# avaiable levels : logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logging.basicConfig(level=logging.DEBUG)
