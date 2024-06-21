import logging

from utils.db import Database
from config import DB_CONFIG
from pipeline import load_raw_dataset, clean_data, optimize_db

LOGGER = logging.getLogger("PIPELINE")

def init_db():
    db = Database(**DB_CONFIG)
    for table in ["combat-attribute",
                  "refresh-area",
                  "job-skill",
                  "hidden-attribute",
                  "tower-boss-attribute",
                  "ordinary-boss-attribute",
                  "pals"]:
        db.delete_table(table_name=table, if_exists=True)
    
    return db

def pipeline():
    LOGGER.info("STARTING PIPELINE PROCESSING ...\n")

    db = init_db()
    load_raw_dataset(db)
    clean_data(db)
    optimize_db(db)
    LOGGER.info("PIPELINE PROCESSED !\n")


if __name__ == "__main__":
    pipeline()
