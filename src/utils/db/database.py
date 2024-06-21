import logging

import pandas as pd

from ._inspector import _DbInspector
from ._connection_manager import _DbConnexionManager


LOGGER = logging.getLogger("DATABASE")

# TODO : ajouter docstrings


class Database:
    def __init__(self, user: str, password: str, host: str, database: str):
        self._db_connexion = _DbConnexionManager(user, password, host, database)

    # PROPERTIES
    @property
    def inspector(self):
        return _DbInspector(self._db_connexion.engine)

    # PRIVATE METHODS
    def _execute(self, query: str, params: dict = {}):
        self._db_connexion.execute(query, params)

    def _generate_select_query(self,
                               table_name: str,
                               column_names: list[str],
                               **kwargs):  # "where", "order_by", "limit"
        query = f"SELECT {', '.join(column_names)} FROM `{table_name}`"
        if "where" in kwargs:
            query += f" WHERE {kwargs['where']}"
        if "order_by" in kwargs:
            query += f" ORDER BY {kwargs['order_by']}"
        if "limit" in kwargs:
            query += f" LIMIT {kwargs['limit']}"
        return query

    # PUBLICS METHODS

    ###########################################################################
    # "Magic" methods :
    ###########################################################################
    def list_columns_names(self, table_name: str):
        return [col["name"] for col in self.inspector.get_columns(table_name)]
    
    def list_table_names(self):
        return self.inspector.get_table_names()
    
    def load_df_as_table(self,
                         df: pd.DataFrame,
                         table_name: str,
                         if_exists: str = "replace"):  # "fail", "replace", "append"
        df.to_sql(table_name,
                  self._db_connexion.engine,
                  if_exists=if_exists,
                  index=False)

    def get_df_from_query(self, query: str):
        return pd.read_sql(query, self._db_connexion.engine)

    ###########################################################################
    # Tables manipulation :
    ###########################################################################
    def create_table_from_select(self,
                                new_table_name: str,
                                select_table_name: str,
                                column_names: list[str],
                                **kwargs):  # "where", "order_by", "limit"
        select_query = self._generate_select_query(table_name=select_table_name,
                                                   column_names=column_names,
                                                   **kwargs)
        query = f"CREATE TABLE IF NOT EXISTS `{new_table_name}` AS {select_query}"
        self._execute(query)

    def delete_table(self, table_name: str, if_exists=True):

        query = f"DROP TABLE "
        if if_exists:
            query += "IF EXISTS "
        query += f"`{table_name}`"
        self._execute(query)
    
    ###########################################################################
    # Columns manipulation :
    ###########################################################################
    def add_column(self,
                   table_name: str,
                   column_name: str,
                   sql_type: str):
        query = f"ALTER TABLE `{table_name}` ADD `{column_name}` {sql_type}"
        self._execute(query)
        
    def create_column_from_select(self,
                                  table_name: str,
                                  column_name: str,
                                  select_table_name: str,
                                  select_column_name: str,
                                  **kwargs):  # "where", "order_by", "limit"
        select_query = self._generate_select_query(table_name=select_table_name,
                                                   column_names=[select_column_name],
                                                   **kwargs)
        query = f"ALTER TABLE `{table_name}` ADD `{column_name}` AS {select_query}"
        self._execute(query)

    def delete_columns(self, table_name: str, column_names: list[str]):
        query = f"ALTER TABLE `{table_name}` "
        query += ", ".join([f"DROP COLUMN `{col}`" for col in column_names])
        self._execute(query)

    def rename_column(self,
                      table_name: str,
                      old_column_name: str,
                      new_column_name: str,
                      sql_type: str | None = None):
        if sql_type is None:
            sql_type = self.inspector.detect_column_sql_type(table_name=table_name,
                                                             column_name=old_column_name)

        query = f"ALTER TABLE `{table_name}` CHANGE `{old_column_name}` `{new_column_name}` {sql_type}"
        self._execute(query)

    def change_column_type(self,
                           table_name: str,
                           column_name: str,
                           sql_type: str):
        query = f"ALTER TABLE `{table_name}` MODIFY `{column_name}` {sql_type}"
        self._execute(query)

    def update_column_from_another_column(self,
                                         dest_table_name,
                                         dest_column_name,
                                         src_table_name,
                                         src_column_name,
                                         src_join_column,
                                         dest_join_column):
        # Build the SQL query to update dest_table
        query = f"""
            UPDATE `{dest_table_name}` AS dest
            JOIN `{src_table_name}` AS src
            ON dest.{dest_join_column} = src.{src_join_column}
            SET dest.{dest_column_name} = src.{src_column_name}
        """
        self._execute(query)

    ############################################################################
    # Rows manipulation :
    ###########################################################################
    def delete_rows(self,
                    table_name: str,
                    where: str = ""):
        query = f"DELETE FROM `{table_name}`"
        if where:
            query += f" WHERE {where}"
        self._execute(query)
    
    def delete_rows_with_nulls(self, 
                               table_name: str,
                               column_name: str):
        self.delete_rows(table_name=table_name,
                         where=f"`{column_name}` IS NULL")

    ###########################################################################
    # Values manipulation :
    ###########################################################################
    def replace_values(self,
                       table_name: str, 
                       column_name: str,
                       value_to_replace: str,
                       new_value: str):
        query = f"UPDATE `{table_name}` SET `{column_name}` = :new_value "
        query += f"WHERE `{column_name}` = :value_to_replace"
        params = {"new_value": new_value, "value_to_replace": value_to_replace}
        self._execute(query, params)

    def strip_left(self,
                   table_name: str,
                   column_name: str,
                   value_to_strip: str):
        query = f"""
        UPDATE `{table_name}`
        SET `{column_name}` = SUBSTRING(`{column_name}`, LOCATE(:value_to_strip, `{column_name}`) + {len(value_to_strip)})
        """
        params = {"value_to_strip": value_to_strip}
        self._execute(query, params)

    def strip_right(self,
                    table_name: str,
                    column_name: str,
                    value_to_strip: str):
        query = f"""
        UPDATE `{table_name}`
        SET `{column_name}` = SUBSTRING(`{column_name}`, 1, LENGTH(`{column_name}`) - LOCATE(:value_to_strip, REVERSE(`{column_name}`)) - LENGTH(:value_to_strip) + 1)
        """
        params = {"value_to_strip": value_to_strip}
        self._execute(query, params)

    def replace_string(self,
                       table_name: str,
                       column_name: str,
                       old_string: str,
                       new_string: str):
        query = f"""
            UPDATE `{table_name}`
            SET `{column_name}` = REPLACE(`{column_name}`, '{old_string}', '{new_string}')
        """
        self._execute(query)

    def replace_nulls(self, table_name: str, column_name: str, value: str):
        query = f"""
            UPDATE `{table_name}`
            SET `{column_name}` = :value
            WHERE `{column_name}` IS NULL
        """
        params = {"value": value}
        self._execute(query, params)

    def replace_yes_null(self, table_name, column_name):
        self.replace_nulls(table_name=table_name,
                           column_name=column_name,
                           value=0)
        self.replace_values(table_name=table_name,
                            column_name=column_name,
                            value_to_replace="yes",
                            new_value=1)
        self.change_column_type(table_name=table_name,
                                column_name=column_name,
                                sql_type="BOOL")

    def replace_TRUE_FALSE(self, table_name: str, column_name: str):
        self.replace_values(table_name=table_name,
                            column_name=column_name,
                            value_to_replace="TRUE",
                            new_value=1)
        self.replace_values(table_name=table_name,
                            column_name=column_name,
                            value_to_replace="FALSE",
                            new_value=0)
        self.change_column_type(table_name=table_name,
                                column_name=column_name,
                                sql_type="BOOL")
    
    ###########################################################################
    # Keys manipulation :
    ###########################################################################
    def create_auto_increment_primary_key_column(self,
                                                 table_name: str,
                                                 column_name: str):
        self.add_column(table_name=table_name,
                        column_name=column_name,
                        sql_type="INT AUTO_INCREMENT PRIMARY KEY")

    def add_foreign_key_constraint(self,
                                   table_name: str,
                                   column_name: str,
                                   reference_table_name: str,
                                   reference_column_name: str):
        query = f"""
            ALTER TABLE `{table_name}`
            ADD CONSTRAINT `fk_{table_name}_{reference_table_name}_{column_name}`
            FOREIGN KEY (`{column_name}`) REFERENCES `{reference_table_name}` (`{reference_column_name}`)
        """
        self._execute(query)

    def add_foreign_key_column(self, 
                               table_name: str,
                               column_name: str,
                               join_column_name: str,
                               reference_table_name: str,
                               reference_column_name: str,
                               reference_join_column_name: str,
                               sql_type: str = "INT"):
        self.add_column(table_name=table_name,
                        column_name=column_name,
                        sql_type=sql_type)
        self.update_column_from_another_column(dest_table_name=table_name,
                                                dest_column_name=column_name,
                                                src_table_name=reference_table_name,
                                                src_column_name=reference_column_name,
                                                src_join_column=reference_join_column_name,
                                                dest_join_column=join_column_name)
        self.add_foreign_key_constraint(table_name=table_name,
                                        column_name=column_name,
                                        reference_table_name=reference_table_name,
                                        reference_column_name=reference_column_name)
