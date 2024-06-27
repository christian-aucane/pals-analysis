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

    # PRIVATE METHODS
    def _execute(self, query: str, params: dict = {}):
        self._db_connexion.execute(query, params)

    # PROPERTIES
    @property
    def inspector(self):
        """
        The inspector of the database

        Inspector methods : 

        - list_table_names() -> list[str]
            Return the names of the tables
        - list_columns(table_name: str) -> list[str]
            Return the names of the columns
        - list_columns_names(table_name: str) -> list[str]
            Return the names of the columns
        - detect_column_sql_type(table_name: str, column_name: str) -> str
            Return the SQL type of the column

        Returns
        -------
        _DbInspector
            The inspector
        """
        return _DbInspector(self._db_connexion.engine)
    
    # PUBLICS METHODS
    ###########################################################################
    # Helpers
    ###########################################################################
    def load_df_as_table(self,
                         df: pd.DataFrame,
                         table_name: str,
                         if_exists: str = "replace"):  # "fail", "replace", "append"
        """
        Load a dataframe as a table in the database
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to load
        table_name : str
            The name of the table
        if_exists : str
            What to do if the table already exists. ["fail", "replace", "append"]
        """
        self._dataframe_manager.load_df_as_table(df, table_name, if_exists)

    def _get_df_from_query(self, query: str):
        """
        Get a dataframe from a query

        Parameters
        ----------
        query : str
            The query to execute

        Returns
        -------
        pd.DataFrame
            The dataframe
        """
        return self._dataframe_manager.get_df_from_query(query)

    def list_table_names(self):
        """
        List the names of the tables in the database

        Returns
        -------
        list[str]
            The names of the tables
        """
        return self.inspector.list_table_names()

    def list_columns_names(self, table_name: str):
        """
        List the names of the columns in the table

        Parameters
        ----------
        table_name : str
            The name of the table

        Returns
        -------
        list[str]
            The names of the columns
        """
        return self.inspector.list_columns_names(table_name=table_name)
    
    ###########################################################################
    # Tables manipulation :
    ###########################################################################
    def create_table_from_select(self,
                                new_table_name: str,
                                select_table_name: str,
                                column_names: list[str],
                                **kwargs):  # "where", "order_by", "limit"
        """
        Create a table from a select query

        Parameters
        ----------
        new_table_name : str
            The name of the new table
        select_table_name : str
            The name of the table to select from
        column_names : list[str]
            The names of the columns to select
        **kwargs
            The parameters of the select query
        """
        select_query = self._sql_generator.generate_select(table_name=select_table_name,
                                                           column_names=column_names,
                                                           **kwargs)
        query = f"CREATE TABLE IF NOT EXISTS `{new_table_name}` AS {select_query}"
        self._execute(query)

    def drop_table(self, table_name: str, if_exists=True):
        """
        Drop a table from the database

        Parameters
        ----------
        table_name : str
            The name of the table to drop
        if_exists : bool
            Whether to drop the table if it exists
        """
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
        """
        Add a column to a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        sql_type : str
            The SQL type of the column
        """
        query = f"ALTER TABLE `{table_name}` ADD `{column_name}` {sql_type}"
        self._execute(query)
        
    def create_column_from_select(self,
                                  table_name: str,
                                  column_name: str,
                                  select_table_name: str,
                                  select_column_name: str,
                                  **kwargs):
        """
        Create a column from a select query

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        select_table_name : str
            The name of the table to select from
        select_column_name : str
            The name of the column to select
        **kwargs
            The parameters of the select query
        """
        select_query = self._sql_generator.generate_select(table_name=select_table_name,
                                                           column_names=[select_column_name],
                                                           **kwargs)
        query = f"ALTER TABLE `{table_name}` ADD `{column_name}` AS {select_query}"
        self._execute(query)

    def delete_columns(self, table_name: str, column_names: list[str]):
        """
        Delete columns from a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_names : list[str]
            The names of the columns to delete
        """
        query = f"ALTER TABLE `{table_name}` "
        query += ", ".join([f"DROP COLUMN `{col}`" for col in column_names])
        self._execute(query)

    def rename_column(self,
                      table_name: str,
                      old_column_name: str,
                      new_column_name: str,
                      sql_type: str | None = None):
        """
        Rename a column in a table

        Parameters
        ----------
        table_name : str
            The name of the table
        old_column_name : str
            The name of the column to rename
        new_column_name : str
            The new name of the column
        sql_type : str
            The SQL type of the column
        """
        if sql_type is None:
            sql_type = self.inspector.detect_column_sql_type(table_name=table_name,
                                                             column_name=old_column_name)

        query = f"ALTER TABLE `{table_name}` CHANGE `{old_column_name}` `{new_column_name}` {sql_type}"
        self._execute(query)

    def change_column_type(self,
                           table_name: str,
                           column_name: str,
                           sql_type: str):
        """
        Change the type of a column in a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        sql_type : str
            The SQL type of the column
        """
        query = f"ALTER TABLE `{table_name}` MODIFY `{column_name}` {sql_type}"
        self._execute(query)

    def update_column_from_another_column(self,
                                         dest_table_name,
                                         dest_column_name,
                                         src_table_name,
                                         src_column_name,
                                         src_join_column,
                                         dest_join_column):
        """
        Update a column from another column in a table

        Parameters
        ----------
        dest_table_name : str
            The name of the table
        dest_column_name : str
            The name of the column
        src_table_name : str
            The name of the table
        src_column_name : str
            The name of the column"""
        # TODO : mettre la création de la requete dans _SqlGenerator
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
        """
        Delete rows from a table

        Parameters
        ----------
        table_name : str
            The name of the table
        where : str
            The condition to delete rows
        """
        query = f"DELETE FROM `{table_name}`"
        if where:
            query += f" WHERE {where}"
        self._execute(query)
    
    def delete_rows_with_nulls(self, 
                               table_name: str,
                               column_name: str):
        """
        Delete rows from a table with null values in a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        """
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
        """
        Replace values in a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        value_to_replace : str
            The value to replace
        new_value : str
            The new value
        """
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
        """
        Strip values from the left of a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        value_to_strip : str
            The value to strip
        """
        new_value = f"SUBSTRING(`{column_name}`, LOCATE('{value_to_strip}', `{column_name}`) + {len(value_to_strip)})"
        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value)
        self._execute(query)

    def strip_right(self,
                    table_name: str,
                    column_name: str,
                    value_to_strip: str):
        """
        Strip values from the right of a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        value_to_strip : str
            The value to strip
        """
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
        """
        Replace a string in a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        old_string : str
            The string to replace
        new_string : str
            The new string
        """
        new_value = f"REPLACE(`{column_name}`, '{old_string}', '{new_string}')"

        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=new_value)
        self._execute(query)

    def replace_nulls(self, table_name: str, column_name: str, value: str):
        """
        Replace null values in a column

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        value : str
            The value to replace
        """
        query = self._sql_generator.generate_update(table_name=table_name,
                                                    column_name=column_name,
                                                    value=value,
                                                    where_column_name=column_name)
        self._execute(query)

    def replace_yes_null(self, table_name, column_name):
        """
        Replace 'yes' and NULL values in a column by 1 and 0 and type BOOL

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        """
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
        """
        Replace 'TRUE' and 'FALSE' values in a column by 1 and 0 and type BOOL

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        """
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
        """
        Create an auto-increment primary key column in a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        """
        self.add_column(table_name=table_name,
                        column_name=column_name,
                        sql_type="INT AUTO_INCREMENT PRIMARY KEY")

    def add_foreign_key_constraint(self,
                                   table_name: str,
                                   column_name: str,
                                   reference_table_name: str,
                                   reference_column_name: str):
        """
        Add a foreign key constraint to a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        reference_table_name : str
            The name of the reference table
        reference_column_name : str
            The name of the reference column
        """
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
        """
        Add a foreign key column to a table

        Parameters
        ----------
        table_name : str
            The name of the table
        column_name : str
            The name of the column
        join_column_name : str
            The name of the join column
        reference_table_name : str
            The name of the reference table
        reference_column_name : str
            The name of the reference column
        reference_join_column_name : str
            The name of the reference join column
        sql_type : str, optional
            The type of the column, by default "INT"
        """
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

    def get_df_from_select(self, table_name: str, columns_names: list[str] | None = None):
        """
        Get a dataframe from a select query

        Parameters
        ----------
        table_name : str
            The name of the table
        columns_names : list[str]
            The names of the columns, by default None (All columns)
        """
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
        """
        Get a dataframe from a join query

        Parameters
        ----------
        left_table_name : str
            The name of the left table
        left_ref_col : str
            The name of the reference column in the left table
        right_table_name : str
            The name of the right table
        right_ref_col : str
            The name of the reference column in the right table
        columns_names : tuple[list[str]] | None, optional
            The names of the columns, by default None (All columns)
        """
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
