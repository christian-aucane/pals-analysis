from src.db import DatabaseConnexion
from src.config import DATA_EXTRACTORS, DB_CONFIG


def extract(table_name):
    return DATA_EXTRACTORS[table_name]()


def process_combat_attribute(df):
    ...

def process_refresh_area(df):
    ...

def process_job_skill(df):
    ...

def process_hiden_attribute(df):
    ...

def process_tower_boss_attribute(df):
    ...

def process_ordinary_boss_attribute(df):
    ...

def pipeline():
    db = DatabaseConnexion(**DB_CONFIG)

    def process(table_name, process_func):
        print(f"Processing {table_name}...")
        df = extract(table_name)
        process_func(df)
        db.load_df_as_table(df, table_name, if_exists="replace")
        print(f"Table loaded in the database successfully.")
    
    process(table_name="combat-attribute", process_func=process_combat_attribute)
    process(table_name="refresh-area", process_func=process_refresh_area)
    process(table_name="job-skill", process_func=process_job_skill)
    process(table_name="hiden-attribute", process_func=process_hiden_attribute)
    process(table_name="tower-boss-attribute", process_func=process_tower_boss_attribute)
    process(table_name="ordinary-boss-attribute", process_func=process_ordinary_boss_attribute)


if __name__ == "__main__":
    pipeline()
