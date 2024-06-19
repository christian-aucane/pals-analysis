import pandas as pd
from db import DatabaseConnexion
from config import DB_CONFIG, CSV_PATHS


def extract(table_name):
    data_extractors = {
        "combat-attribute": lambda: pd.read_csv(CSV_PATHS["combat-attribute"], skiprows=1),
        "refresh-area": lambda: pd.read_csv(CSV_PATHS["refresh-area"], skiprows=4),
        "job-skill": lambda: pd.read_csv(CSV_PATHS["job-skill"], skiprows=1),
        "hidden-attribute": lambda: pd.read_csv(CSV_PATHS["hidden-attribute"]),
        "tower-boss-attribute": lambda: pd.read_csv(CSV_PATHS["tower-boss-attribute"], index_col="name").T,
        "ordinary-boss-attribute": lambda: pd.read_csv(CSV_PATHS["ordinary-boss-attribute"],  skiprows=3)
    }
    return data_extractors[table_name]()


def load_data(db):

    def process(table_name):
        # TODO : sortir la fonction d'ici ?
        print(f"PROCESSING TABLE '{table_name}'...")
        # Extract
        print("Extracting data...")
        df = extract(table_name)
        # Load
        print("Loading data in the database...")
        db.load_df_as_table(df, table_name, if_exists="replace")

        print("Done !\n")

    process(table_name="combat-attribute")
    process(table_name="refresh-area")
    process(table_name="job-skill")
    process(table_name="hidden-attribute")
    process(table_name="tower-boss-attribute")
    process(table_name="ordinary-boss-attribute")

def transform_combat_attribute(db):
    # Delete columns
    empty_cols = ["OverrideNameTextID",
                  "NamePrefixID",
                  "OverridePartnerSkillTextID",
                  "AISightResponse"]
    useless_cols = ["IsPal",
                    "CodeName",
                    "Tribe",
                    "Organization",
                    "weapon",
                    "WeaponEquip"]
    db.delete_columns(table_name="combat-attribute", column_names=empty_cols + useless_cols)
    
    db.rename_column(table_name="combat-attribute", old_column_name="BPCLass", new_column_name="Tribe")

    # nocturnal / Variant
    for col in ["nocturnal", "Variant"]:
        db.replace_nulls(table_name="combat-attribute", column_name=col, value=0)
        db.replace_values(table_name="combat-attribute", column_name=col, value_to_replace="yes", new_value=1)
        db.change_type(table_name="combat-attribute", column_name="nocturnal", new_column_type=bool)

    # Riding sprint speed
    db.replace_nulls(table_name="combat-attribute", column_name="Riding sprint speed", value=0)
    db.change_type(table_name="combat-attribute", column_name="Riding sprint speed", new_column_type=int)

    # Genus Category
    db.replace_string(table_name="combat-attribute", column_name="GenusCategory", old_string="EPalGenusCategoryType::", new_string="")

    # (being) damage multiplier / catch rate / Experience multiplier
    for col in ["(being) damage multiplier", "catch rate", "Experience multiplier"]:
        db.replace_string(table_name="combat-attribute", column_name=col, old_string="%", new_string="")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"{col}_percent", new_column_type=int)

    # lvl1 / lvl2 / lvl3 / lvl4 / lvl5
    for col in ["lv1", "lv2", "lv3", "lv4", "lv5"]: # BE CAREFUL ! BAD CHARTERS !  not 'lvl'
        db.strip_right(table_name="combat-attribute", column_name=col, value_to_strip="(")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"lvl{col[2:]}", new_column_type=float) # Bad characters not 'lvl


def transform_data(db):
    transform_combat_attribute(db)


def pipeline():
    db = DatabaseConnexion(**DB_CONFIG)
    load_data(db)
    transform_data(db)


if __name__ == "__main__":
    pipeline()
