
import logging

from .extract_raw_data import extract_raw_data


LOGGER = logging.getLogger("DATA LOADING")

def load_data(db):

    def load(table_name):
        # TODO : sortir la fonction d'ici ?
        LOGGER.info(f"LOADING TABLE '{table_name}'...")
        # Extract
        df = extract_raw_data(table_name)
        # Load
        db.load_df_as_table(df, table_name, if_exists="replace")

        LOGGER.info("Done !\n")

    load(table_name="combat-attribute")
    load(table_name="refresh-area")
    load(table_name="job-skill")
    load(table_name="hidden-attribute")
    load(table_name="tower-boss-attribute")
    load(table_name="ordinary-boss-attribute")
    