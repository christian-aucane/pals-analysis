import logging

import pandas as pd
from utils.db import DatabaseConnexion
from config import DB_CONFIG
from pipeline import load_raw_dataset, clean_db

LOGGER = logging.getLogger("PIPELINE")

def pipeline():
    LOGGER.info("STARTING PIPELINE PROCESSING ...\n")

    db = DatabaseConnexion(**DB_CONFIG)
    load_raw_dataset(db)
    clean_db(db)

    LOGGER.info("PIPELINE PROCESSED !\n")


if __name__ == "__main__":
    pipeline()
