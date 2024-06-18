from pathlib import Path


# TODO : move config in .env file
DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "palworld_database",
}


RAW_DATA_DIR = Path(__file__).resolve().parent / "raw_data"
CSV_PATHS = {
    "combat-attribute": RAW_DATA_DIR / "Palworld_Data--Palu combat attribute table.csv",
    "refresh-level": RAW_DATA_DIR / "Palworld_Data--Palu refresh level.csv",
    "job-skills": RAW_DATA_DIR / "Palworld_Data-Palu Job Skills Table.csv",
    "hiden-attributes": RAW_DATA_DIR / "Palworld_Data-hide Pallu attributes.csv",
    "tower-boss-attribute": RAW_DATA_DIR / "Palworld_Data-Tower BOSS attribute comparison.csv",
    "ordinary-boss-attribute": RAW_DATA_DIR / "Palworld_Data-comparison of ordinary BOSS attributes.csv",
}
