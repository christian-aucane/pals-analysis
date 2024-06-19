import pandas as pd

from config import CSV_PATHS


def extract_combat_attribute():
    # Skip first row because it contain text
    return pd.read_csv(CSV_PATHS["combat-attribute"], skiprows=1)


def extract_refresh_area():
    # Skip first 4 rows because it contain text
    return pd.read_csv(CSV_PATHS["refresh-area"], skiprows=4)


def extract_job_skill():
    # Skip first row because it contain text
    return pd.read_csv(CSV_PATHS["job-skill"], skiprows=1)


def extract_hidden_attribute():
    # Just read CSV
    return pd.read_csv(CSV_PATHS["hidden-attribute"])


def extract_tower_boss_attribute():
    # Transpose and reset index
    return pd.read_csv(CSV_PATHS["tower-boss-attribute"],
                        index_col="name").T.reset_index().rename(columns={"index": "name"})


def extract_ordinary_boss_attribute():
    # Skip first 3 rows because it contain text
    return pd.read_csv(CSV_PATHS["ordinary-boss-attribute"],  skiprows=3)


def extract_raw_data(table_name):
    # Manipulations to extract data correctly
    data_extractors = {
        "combat-attribute": extract_combat_attribute,
        "refresh-area": extract_refresh_area,
        "job-skill": extract_job_skill,
        "hidden-attribute": extract_hidden_attribute,
        "tower-boss-attribute": extract_tower_boss_attribute,
        "ordinary-boss-attribute": extract_ordinary_boss_attribute
    }
    return data_extractors[table_name]()
