import logging

from utils.db import Database
from config import DB_CONFIG
from pipeline import load_raw_dataset, clean_data

LOGGER = logging.getLogger("PIPELINE")

def pipeline():
    LOGGER.info("STARTING PIPELINE PROCESSING ...\n")

    db = Database(**DB_CONFIG)
    load_raw_dataset(db)
    clean_data(db)


    LOGGER.info("PIPELINE PROCESSED !\n")


if __name__ == "__main__":
    pipeline()
