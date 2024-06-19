import logging

import pandas as pd
from utils.db import DatabaseConnexion
from config import DB_CONFIG
from pipeline.clean_data import clean_data
from pipeline.load_data import load_dataset

LOGGER = logging.getLogger("PIPELINE")

def pipeline():
    LOGGER.info("STARTING PIPELINE PROCESSING ...\n")

    db = DatabaseConnexion(**DB_CONFIG)
    load_dataset(db)
    clean_data(db)

    LOGGER.info("PIPELINE PROCESSED !\n")


if __name__ == "__main__":
    pipeline()
