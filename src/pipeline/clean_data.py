import logging

LOGGER = logging.getLogger("DATA CLEANING")

def clean_combat_attribute(db):
    LOGGER.info("Transforming combat-attribute...")
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
        db.replace_yes_null(table_name="combat-attribute", column_name=col)

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

    LOGGER.info("Done !\n")

def clean_refresh_area(db):
    LOGGER.info("Transforming refresh-area...")
    empty_cols = ["Unnamed: 4",
                  "Unnamed: 12"]

    db.delete_columns(table_name="refresh-area", column_names=empty_cols)

    # Type INT
    for col in ["ID", "minimum level", "maximum level", "ID.2"]:
        db.change_type(table_name="refresh-area", column_name=col, new_column_type=int)

    # Replace yes null
    for col in ["Night only", "Night only.1"]:
        db.replace_yes_null(table_name="refresh-area", column_name=col)

    LOGGER.info("Done !\n")

def clean_job_skill(db):
    LOGGER.info("Transforming job-skill...")
    empty_cols = ["Handling speed",
                  "ranch items",
                  "pasture minimum output",
                  "The largest ranch (Rank = partner skill level)"]

    db.delete_columns(table_name="job-skill", column_names=empty_cols)

    db.replace_yes_null(table_name="job-skill", column_name="night shift")

    LOGGER.info("Done !\n")

def clean_hidden_attribute(db):
    LOGGER.info("Transforming hidden-attribute...")
    empty_cols = ["ZukanIndexSuffix",
                  "AISightResponse"]
    useless_cols = ["IsPal",
                    "Organization",
                    "weapon",
                    "WeaponEquip",
                    "BPCLass"]

    db.delete_columns(table_name="hidden-attribute", column_names=empty_cols + useless_cols)

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

    for col in ["(being) damage multiplier", "Capture probability"]:
        db.replace_string(table_name="hidden-attribute", column_name=col, old_string="%", new_string="")
        db.rename_column(table_name="hidden-attribute", old_column_name=col, new_column_name=f"{col}_percent", new_column_type=int)    

    LOGGER.info("Done !\n")

def clean_tower_boss_attribute(db):
    LOGGER.info("Transforming tower-boss-attribute...")

    # BOOL
    for col in ["Ignore the bluntness", "Ignore displacement"]:
        db.replace_TRUE_FALSE(table_name="tower-boss-attribute", column_name=col)

    # INT
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

    LOGGER.info("Done !\n")

def clean_ordinary_boss_attribute(db):
    LOGGER.info("Transforming ordinary-boss-attribute...")
    empty_cols = ["Unnamed: 2",
                  "Unnamed: 5"]
    db.delete_columns(table_name="ordinary-boss-attribute", column_names=empty_cols)

    # INT
    for col in ["HP", "Remote attack"]:
        db.change_type(table_name="ordinary-boss-attribute", column_name=col, new_column_type=int)

    LOGGER.info("Done !\n")

def clean_data(db):
    clean_combat_attribute(db)
    clean_refresh_area(db)
    clean_job_skill(db)
    clean_hidden_attribute(db)
    clean_tower_boss_attribute(db)
    clean_ordinary_boss_attribute(db)
