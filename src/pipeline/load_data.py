
import logging

from .extract_raw_data import extract_raw_data


LOGGER = logging.getLogger("DATA LOADING")


def load(db, table_name):
    LOGGER.info(f"TABLE '{table_name}'...")

    # Extract
    df = extract_raw_data(table_name)
    # Load
    db.load_df_as_table(df, table_name, if_exists="replace")

    LOGGER.info("TABLE LOADED !\n")

def load_dataset(db):
    LOGGER.info("DATASET...\n")
    
    load(db=db, table_name="combat-attribute")
    load(db=db, table_name="refresh-area")
    load(db=db, table_name="job-skill")
    load(db=db, table_name="hidden-attribute")
    load(db=db, table_name="tower-boss-attribute")
    load(db=db, table_name="ordinary-boss-attribute")

    LOGGER.info("DATASET LOADED !\n")
    