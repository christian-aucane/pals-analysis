from pathlib import Path

import pandas as pd

from db import DataframeToDatabaseLoader

from constants import CSV_PATHS, DB_CONFIG


def palu_combat_attribute_pipeline(loader):
    # Extract
    df = pd.read_csv(CSV_PATHS["combat-attribute"], skiprows=1)

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "combat-attribute")

def palu_refresh_level_pipeline(loader):
    # Extract
    df = pd.read_csv(CSV_PATHS["refresh-level"], skiprows=4)

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "refresh-area")

def palu_job_skills_pipeline(loader):
    # Extract
    df = pd.read_csv(CSV_PATHS["job-skills"], skiprows=1)

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "job-skill")

def palu_hide_attributes_pipeline(loader):
    # Extract
    df = pd.read_csv(CSV_PATHS["hiden-attributes"])

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "hidden-attribute")

def tower_boss_attribute_comparison_pipeline(loader):

    # Extract
    df = pd.read_csv(CSV_PATHS["tower-boss-attribute"], index_col="name").T

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "tower-boss-attribute")

def ordinary_boss_attribute_comparison_pipeline(loader):

    # Extract
    df = pd.read_csv(CSV_PATHS["ordinary-boss-attribute"], skiprows=3)

    # Transform
    # TODO : process df

    # Load
    loader.load(df, "ordinary-boss-attribute")


def pipeline():
    loader = DataframeToDatabaseLoader(**DB_CONFIG)

    palu_combat_attribute_pipeline(loader)
    palu_refresh_level_pipeline(loader)
    palu_job_skills_pipeline(loader)
    palu_hide_attributes_pipeline(loader)
    tower_boss_attribute_comparison_pipeline(loader)
    ordinary_boss_attribute_comparison_pipeline(loader)


if __name__ == "__main__":
    pipeline()
