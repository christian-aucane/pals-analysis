import logging

from utils.db import Database


LOGGER = logging.getLogger("OPTIMIZING DATABASE")


def create_pals_table(db: Database):
    LOGGER.info("CREATING TABLE 'pals'...\n")
    columns = [
        "id",
        "name",
        "chinese_name",
        "volume_size",
        "tribe",
        "genus_category",
        "price",
        "rarity",
        "element_1",
        "element_2",
        "variant",
    ]

    db.create_table_from_select(new_table_name="pals",
                                select_table_name="combat-attribute",
                                column_names=columns)
    db.rename_column(table_name="pals",
                     old_column_name="id",
                     new_column_name="pal_id")



def add_combat_attribute_relationships(db: Database):
    db.add_foreign_key_column(table_name="combat-attribute",
                              column_name="unique_id",
                              join_column_name="name",
                              reference_table_name="pals",
                              reference_column_name="unique_id",
                              reference_join_column_name="name")

    columns_to_delete = [
        "id",
        "name",
        "chinese_name",
        "volume_size",
        "tribe",
        "genus_category",
        "price",
        "rarity",
        "element_1",
        "element_2",
        "variant",
    ]
    db.delete_columns(table_name="combat-attribute", column_names=columns_to_delete)

def add_job_skill_relationships(db: Database):
    db.add_foreign_key_column(table_name="job-skill",
                              column_name="unique_id",
                              join_column_name="english_name",
                              reference_table_name="pals",
                              reference_column_name="unique_id",
                              reference_join_column_name="name",
                              sql_type="INT NOT NULL")
    columns_to_delete = [
        "id",
        "english_name",
        "chinese_name",
        "volume_size",
    ]
    db.delete_columns(table_name="job-skill", column_names=columns_to_delete)

def add_refresh_area_relationships(db: Database):
    db.add_foreign_key_column(table_name="refresh-area",
                              column_name="unique_id",
                              join_column_name="name",
                              reference_table_name="pals",
                              reference_column_name="unique_id",
                              reference_join_column_name="chinese_name")

    columns_to_delete = ["id", "name"]
    db.delete_columns(table_name="refresh-area", column_names=columns_to_delete)


def add_relationships(db: Database):
    LOGGER.info("ADDING RELATIONSHIPS...\n")
    
    db.create_auto_increment_primary_key_column(table_name="pals", column_name="unique_id")

    # combat-attribute -> pals
    add_combat_attribute_relationships(db)

    # job-skill -> pals
    add_job_skill_relationships(db)

    # refresh-area -> pals
    add_refresh_area_relationships(db)


    # hidden-attribute -> pals


    
    LOGGER.info("RELATIONSHIPS ADDED !\n")


def optimize_db(db: Database):
    LOGGER.info("OPTIMIZING DATABASE...\n")
    create_pals_table(db)
    add_relationships(db)
    LOGGER.info("DATABASE OPTIMIZED !\n")