import logging

from utils.db import Database
from utils.regex import normalize_special_cases, remove_special_characters, camel_case_to_snake_case


LOGGER = logging.getLogger("DATA CLEANING")

def clean_combat_attribute(db: Database):
    LOGGER.info("TABLE combat-attribute...")

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
    
    # Rename columns
    db.rename_column(table_name="combat-attribute", old_column_name="BPClass", new_column_name="Tribe")

    # Replace yes and null with true and false (BOOL)
    for col in ["nocturnal", "Variant"]:
        db.replace_yes_null(table_name="combat-attribute", column_name=col)

    # Replace null with 0
    db.replace_nulls(table_name="combat-attribute", column_name="Riding sprint speed", value=0)
    db.change_type(table_name="combat-attribute", column_name="Riding sprint speed", sql_type="INT")

    # Remove EPalGenusCategoryType::
    db.replace_string(table_name="combat-attribute",
                      column_name="GenusCategory",
                      old_string="EPalGenusCategoryType::",
                      new_string="")

    # Remove %, rename with _percent and type INT
    for col in ["(being) damage multiplier", "catch rate", "Experience multiplier"]:
        db.replace_string(table_name="combat-attribute", column_name=col, old_string="%", new_string="")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"{col}_percent", sql_type="INT")

    # Remove end parenthesis, rename with normals characters and type FLOAT
    for col in ["lv1", "lv2", "lv3", "lv4", "lv5"]: # BE CAREFUL ! BAD CHARTERS !  not 'lvl'
        db.strip_right(table_name="combat-attribute", column_name=col, value_to_strip="(")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"lvl{col[2:]}", sql_type="FLOAT") # Bad characters not 'lvl

    LOGGER.info("TABLE CLEANED !\n")

def clean_refresh_area(db: Database):
    LOGGER.info("TABLE refresh-area...")

    # Delete columns
    empty_cols = ["Unnamed: 4",
                  "Unnamed: 12"]
    useless_cols = [
        "ID.1",
        "name.1",
        "minimum level.1",
        "maximum level.1",
        "Pallu refresh type.1",
        "Night only.1",
        "refresh area.1",
        "ID.2",
        "name.2",
    ]
    db.delete_columns(table_name="refresh-area", column_names=empty_cols + useless_cols)

    # Delete empty rows
    db.delete_rows_with_nulls(table_name="refresh-area", column_name="ID")
    
    # Type INT
    for col in ["ID", "minimum level", "maximum level"]:
        db.change_type(table_name="refresh-area", column_name=col, sql_type="INT")

    # Replace yes null with true and false (BOOL)
    for col in ["Night only"]:
        db.replace_yes_null(table_name="refresh-area", column_name=col)

    LOGGER.info("TABLE CLEANED !\n")

def clean_job_skill(db: Database):
    LOGGER.info("TABLE job-skill...")

    # Delete columns
    empty_cols = ["Handling speed",
                  "ranch items",
                  "pasture minimum output",
                  "The largest ranch (Rank = partner skill level)"]
    db.delete_columns(table_name="job-skill", column_names=empty_cols)

    # Replace yes null with true and false (BOOL)
    db.replace_yes_null(table_name="job-skill", column_name="night shift")

    LOGGER.info("TABLE CLEANED !\n")

def clean_hidden_attribute(db: Database):
    LOGGER.info("TABLE hidden-attribute...")

    # Delete columns
    empty_cols = ["ZukanIndexSuffix",
                  "AISightResponse"]
    useless_cols = ["IsPal",
                    "Organization",
                    "weapon",
                    "WeaponEquip",
                    "BPCLass"]
    db.delete_columns(table_name="hidden-attribute", column_names=empty_cols + useless_cols)

    # Remove useless substrings
    db.replace_string(table_name="hidden-attribute",
                      column_name="OverrideNameTextID",
                      old_string="PAL_NAME_",
                      new_string="")
    db.replace_string(table_name="hidden-attribute",
                      column_name="OverridePartnerSkillTextID",
                      old_string="PARTNERSKILL_",
                      new_string="")
    for col in ["Tribe", "GenusCategory", "BattleBGM"]:
        db.strip_left(table_name="hidden-attribute", column_name=col, value_to_strip="::")

    # Remove %, rename with _percent and type INT
    for col in ["(being) damage multiplier", "Capture probability"]:
        db.replace_string(table_name="hidden-attribute", column_name=col, old_string="%", new_string="")
        db.rename_column(table_name="hidden-attribute", old_column_name=col, new_column_name=f"{col}_percent", sql_type="INT")    

    LOGGER.info("TABLE CLEANED !\n")

def clean_tower_boss_attribute(db: Database):
    LOGGER.info("TABLE tower-boss-attribute...")

    # Type BOOL
    for col in ["Ignore the bluntness", "Ignore displacement"]:
        db.replace_TRUE_FALSE(table_name="tower-boss-attribute", column_name=col)

    # Type INT
    for col in ["HP", 
                "melee attack",
                "Remote attack",
                "defense",
                "Support",
                "experience ratio",
                "slow walking speed",
                "walking speed",
                "running speed",
                "riding speed",
                "Handling speed",
                "BiologicalGrade",
                "endurance",
                "fecundity"]:
        db.change_type(table_name="tower-boss-attribute", column_name=col, sql_type="INT")

    LOGGER.info("TABLE CLEANED !\n")

def clean_ordinary_boss_attribute(db: Database):
    LOGGER.info("TABLE ordinary-boss-attribute...")

    # Delete columns
    empty_cols = ["Unnamed: 2",
                  "Unnamed: 5"]
    db.delete_columns(table_name="ordinary-boss-attribute", column_names=empty_cols)

    # Type INT
    for col in ["HP", "Remote attack"]:
        db.change_type(table_name="ordinary-boss-attribute", column_name=col, sql_type="INT")

    LOGGER.info("TABLE CLEANED !\n")


def normalize_column_names(db: Database):
    SPECIAL_CASES = {
        "ID": "id",
        "HP": "hp",
        "4D": "4d",
        "AIRResponse": "air_response",
        "lvl1": "lvl_1",
        "lvl2": "lvl_2",
        "lvl3": "lvl_3",
        "lvl4": "lvl_4",
        "lvl5": "lvl_5",
    }

    def normalize_column_name(column_name: str):
        column_name = normalize_special_cases(column_name, SPECIAL_CASES)
        column_name = remove_special_characters(column_name, replace_with="_")
        column_name = camel_case_to_snake_case(column_name)
        column_name = column_name.strip('_').lower().replace("__", "_")
        return column_name

    table_names = db.list_table_names()
    for table_name in table_names:
        columns = db.list_columns_names(table_name)
        for col in columns:
            normalized_col = normalize_column_name(col)
            if normalized_col != col:
                db.rename_column(table_name, col, normalized_col)


def clean_data(db: Database):
    LOGGER.info("CLEANING DATA...\n")

    clean_combat_attribute(db)
    clean_refresh_area(db)
    clean_job_skill(db)
    clean_hidden_attribute(db)
    clean_tower_boss_attribute(db)
    clean_ordinary_boss_attribute(db)

    normalize_column_names(db)

    LOGGER.info("DATA CLEANED !\n")
