import pandas as pd

from config import CSV_PATHS

def extract_raw_data(table_name):
    # Manipulations to extract data correctly
    data_extractors = {
        "combat-attribute": lambda: pd.read_csv(CSV_PATHS["combat-attribute"], skiprows=1),
        "refresh-area": lambda: pd.read_csv(CSV_PATHS["refresh-area"], skiprows=4),
        "job-skill": lambda: pd.read_csv(CSV_PATHS["job-skill"], skiprows=1),
        "hidden-attribute": lambda: pd.read_csv(CSV_PATHS["hidden-attribute"]),
        "tower-boss-attribute": lambda: pd.read_csv(CSV_PATHS["tower-boss-attribute"],
                                                    index_col="name").T.reset_index().rename(columns={"index": "name"}),
        "ordinary-boss-attribute": lambda: pd.read_csv(CSV_PATHS["ordinary-boss-attribute"],  skiprows=3)
    }
    return data_extractors[table_name]()
