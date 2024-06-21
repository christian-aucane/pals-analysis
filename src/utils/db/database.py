import logging

import pandas as pd

try:
    
    from ._inspector import _DbInspector
    from ._connection_manager import _DbConnexionManager
    from ._sql_generator import _SqlGenerator
    from ._dataframe_manager import _DataframeManager
except ImportError:
    from _inspector import _DbInspector
    from _connection_manager import _DbConnexionManager
    from _sql_generator import _SqlGenerator
    from _dataframe_manager import _DataframeManager

LOGGER = logging.getLogger("DATABASE")

# TODO : ajouter docstrings


class Database:
    _sql_generator = _SqlGenerator()

    def __init__(self, user: str, password: str, host: str, database: str):
        self._db_connexion = _DbConnexionManager(user, password, host, database)
        self._dataframe_manager = _DataframeManager(self._db_connexion)

    # PROPERTIES
    @property
    def inspector(self):
        return _DbInspector(self._db_connexion.engine)

    # PRIVATE METHODS
    def _execute(self, query: str, params: dict = {}):
        self._db_connexion.execute(query, params)

    # PUBLICS METHODS
    
    ###########################################################################
    # "Magic" methods :
    ###########################################################################
    def load_df_as_table(self,
                         df: pd.DataFrame,
                         table_name: str,
                         if_exists: str = "replace"):  # "fail", "replace", "append"
        self._dataframe_manager.load_df_as_table(df, table_name, if_exists)

    def _get_df_from_query(self, query: str):
        return self._dataframe_manager.get_df_from_query(query)

    ###########################################################################
    # Tables manipulation :
    ###########################################################################
    def create_table_from_select(self,
                                new_table_name: str,
                                select_table_name: str,
                                column_names: list[str],
                                **kwargs):  # "where", "order_by", "limit"
        select_query = self._sql_generator.generate_select(table_name=select_table_name,
                                                           column_names=column_names,
                                                           **kwargs)
        query = f"CREATE TABLE IF NOT EXISTS `{new_table_name}` AS {select_query}"
        self._execute(query)

    def drop_table(self, table_name: str, if_exists=True):
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
        select_query = self._sql_generator.generate_select(table_name=select_table_name,
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
        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value,
                                                    where_column_name=column_name,
                                                    where_value=value_to_replace)
        self._execute(query)

    def strip_left(self,
                   table_name: str,
                   column_name: str,
                   value_to_strip: str):
        new_value = f"SUBSTRING(`{column_name}`, LOCATE('{value_to_strip}', `{column_name}`) + {len(value_to_strip)})"

        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value)
        self._execute(query)

    def strip_right(self,
                    table_name: str,
                    column_name: str,
                    value_to_strip: str):
        new_value = f"SUBSTRING(`{column_name}`, 1, LENGTH(`{column_name}`) - LOCATE('{value_to_strip}', REVERSE(`{column_name}`)) - LENGTH('{value_to_strip}') + 1)"
        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value)
        self._execute(query)

    def replace_string(self,
                       table_name: str,
                       column_name: str,
                       old_string: str,
                       new_string: str):
        new_value = f"REPLACE(`{column_name}`, '{old_string}', '{new_string}')"

        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value)
        self._execute(query)

    def replace_nulls(self, table_name: str, column_name: str, value: str):
        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=value,
                                                    where_column_name=column_name)
        self._execute(query)

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

    ###########################################################################
    # Data reading
    ###########################################################################

    def get_df_from_select(self, table_name: str, columns_names: list[str]):
        query = self._sql_generator.generate_select(table_name=table_name,
                                                    columns_names=columns_names)
        print("columns names : ", columns_names)
        print(f"Query : {query}")
        return self._get_df_from_query(query)
    
    def get_df_from_join(self,
                         left_table_name: str,
                         left_ref_col: str,
                         right_table_name: str,
                         right_ref_col: str,
                         columns_names: tuple[list[str]] | None = None):
        query = self._sql_generator.generate_select_join(left_table_name=left_table_name,
                                                         left_ref_col=left_ref_col,
                                                         right_table_name=right_table_name,
                                                         right_ref_col=right_ref_col,
                                                         columns_names=columns_names)
        print("columns names : ", columns_names)
        print(f"Query : {query}")
        return self._get_df_from_query(query)
    

if __name__ == "__main__":
    db = Database(user="root", password="root", host="localhost", database="palworld_database")

    # print(db.get_df_from_select(table_name="pals", columns_names=["pal_id", "name"]))

    print(db.get_df_from_join(left_table_name="pals",
                              left_ref_col="unique_id",
                              right_table_name="combat-attribute",
                              right_ref_col="unique_id",
                              columns_names=(["pal_id", "name"], ["lvl_1"])))
