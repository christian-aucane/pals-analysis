import logging

import pandas as pd
from utils.db import DatabaseConnexion
from config import DB_CONFIG
from pipeline.clean_data import clean_data
from pipeline.load_data import load_data

LOGGER = logging.getLogger("PIPELINE")

def pipeline():
    db = DatabaseConnexion(**DB_CONFIG)
    load_data(db)
    clean_data(db)


if __name__ == "__main__":
    pipeline()
