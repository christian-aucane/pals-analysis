import logging

from utils.db import DatabaseConnexion


LOGGER = logging.getLogger("DATA CLEANING")


def clean_combat_attribute(db: DatabaseConnexion):
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
    db.rename_column(table_name="combat-attribute", old_column_name="BPCLass", new_column_name="Tribe")

    # Replace yes and null with true and false (BOOL)
    for col in ["nocturnal", "Variant"]:
        db.replace_yes_null(table_name="combat-attribute", column_name=col)

    # Replace null with 0
    db.replace_nulls(table_name="combat-attribute", column_name="Riding sprint speed", value=0)
    db.change_type(table_name="combat-attribute", column_name="Riding sprint speed", new_column_type=int)

    # Remove EPalGenusCategoryType::
    db.replace_string(table_name="combat-attribute",
                      column_name="GenusCategory",
                      old_string="EPalGenusCategoryType::",
                      new_string="")

    # Remove %, rename with _percent and type INT
    for col in ["(being) damage multiplier", "catch rate", "Experience multiplier"]:
        db.replace_string(table_name="combat-attribute", column_name=col, old_string="%", new_string="")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"{col}_percent", new_column_type=int)

    # Remove end parenthesis, rename with normals characters and type FLOAT
    for col in ["lv1", "lv2", "lv3", "lv4", "lv5"]: # BE CAREFUL ! BAD CHARTERS !  not 'lvl'
        db.strip_right(table_name="combat-attribute", column_name=col, value_to_strip="(")
        db.rename_column(table_name="combat-attribute", old_column_name=col, new_column_name=f"lvl{col[2:]}", new_column_type=float) # Bad characters not 'lvl

    LOGGER.info("TABLE CLEANED !\n")

def clean_refresh_area(db: DatabaseConnexion):
    LOGGER.info("TABLE refresh-area...")

    # Delete columns
    empty_cols = ["Unnamed: 4",
                  "Unnamed: 12"]
    db.delete_columns(table_name="refresh-area", column_names=empty_cols)

    # Type INT
    for col in ["ID", "minimum level", "maximum level", "ID.2"]:
        db.change_type(table_name="refresh-area", column_name=col, new_column_type=int)

    # Replace yes null with true and false (BOOL)
    for col in ["Night only", "Night only.1"]:
        db.replace_yes_null(table_name="refresh-area", column_name=col)

    LOGGER.info("TABLE CLEANED !\n")

def clean_job_skill(db: DatabaseConnexion):
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

def clean_hidden_attribute(db: DatabaseConnexion):
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
        db.rename_column(table_name="hidden-attribute", old_column_name=col, new_column_name=f"{col}_percent", new_column_type=int)    

    LOGGER.info("TABLE CLEANED !\n")

def clean_tower_boss_attribute(db: DatabaseConnexion):
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
        db.change_type(table_name="tower-boss-attribute", column_name=col, new_column_type=int)

    LOGGER.info("TABLE CLEANED !\n")

def clean_ordinary_boss_attribute(db: DatabaseConnexion):
    LOGGER.info("TABLE ordinary-boss-attribute...")

    # Delete columns
    empty_cols = ["Unnamed: 2",
                  "Unnamed: 5"]
    db.delete_columns(table_name="ordinary-boss-attribute", column_names=empty_cols)

    # Type INT
    for col in ["HP", "Remote attack"]:
        db.change_type(table_name="ordinary-boss-attribute", column_name=col, new_column_type=int)

    LOGGER.info("TABLE CLEANED !\n")

def clean_db(db: DatabaseConnexion):
    LOGGER.info("CLEANING DATA...\n")

    clean_combat_attribute(db)
    clean_refresh_area(db)
    clean_job_skill(db)
    clean_hidden_attribute(db)
    clean_tower_boss_attribute(db)
    clean_ordinary_boss_attribute(db)

    LOGGER.info("DATA CLEANED !\n")
