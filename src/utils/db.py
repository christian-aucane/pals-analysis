import logging
from functools import reduce

import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError

LOGGER = logging.getLogger("DATABASE")

# TODO : ajouter docstrings

class DbConnexionManager:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = None
        self.connection = None
        self._connect()

    def __del__(self):
        self._close()

    # PRIVATE METHODS
    def _connect(self):
        LOGGER.info("CONNECTING ...\n")
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')
        self.connection = self.engine.connect()
        self.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.execute(f"USE {self.database}")

    def _close(self):
        LOGGER.info("CLOSING CONNECTION ...\n")
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.engine:
            self.engine.dispose()
            self.engine = None

    # PUBLIC METHOD
    def execute(self, query, params={}):
        # TODO : ajouter optimisation du nb de connexions et de requetes
        
        formatted_query = reduce(lambda q, kv: q.replace(f":{kv[0]}", f"'{kv[1]}'"), params.items(), query)
        LOGGER.debug(f"Executing query : {formatted_query}")
        try:
            self.connection.execute(text(query), params)
            self.connection.commit()
        except OperationalError as e:
            LOGGER.error(e)


class Database:
    def __init__(self, user, password, host, database):
        self._db_connexion = DbConnexionManager(user, password, host, database)

    # PROPERTIES
    @property
    def inspector(self):
        # TODO : create an inspector class from scratch ?
        return inspect(self._db_connexion.engine)

    # PRIVATE METHODS
    def _execute(self, query, params={}):
        self._db_connexion.execute(query, params)

    @staticmethod
    def _python_to_sql_type(column_type: type):
        python_to_sql = {bool: "TINYINT(1)", int: "INT", float: "FLOAT", str: "TEXT"}
        try:
            return python_to_sql[column_type]
        except KeyError:
            raise ValueError(f"Unknown column type : {column_type} - Only {' '.join(map(str, python_to_sql.keys()))} are supported")
        
    def _detect_column_sql_type(self, table_name, column_name):
        column_info = self.inspector.get_columns(table_name)
        column_type = None

        for col in column_info:
            if col["name"] == column_name:
                column_type = col["type"]
                break
        if column_type is None:
            raise ValueError(f"Column '{column_name}' not found in table '{table_name}'")
        return column_type

    # PUBLICS METHODS
    def inspect_columns(self, table_name):
        return self.inspector.get_columns(table_name)
    
    def list_columns_names(self, table_name):
        return [col["name"] for col in self.inspector.get_columns(table_name)]
    
    def list_table_names(self):
        return self.inspector.get_table_names()
    
    def load_df_as_table(self, df, table_name, if_exists="replace"):
        df.to_sql(table_name, self._db_connexion.engine, if_exists=if_exists, index=False)

    def get_df_from_query(self, query):
        return pd.read_sql(query, self._db_connexion.engine)

    def delete_columns(self, table_name, column_names):
        query = f"ALTER TABLE `{table_name}` " + ", ".join([f"DROP COLUMN `{col}`" for col in column_names])
        self._execute(query)
    
    def replace_values(self, table_name, column_name, value_to_replace, new_value):
        query = f"UPDATE `{table_name}` SET `{column_name}` = :new_value WHERE `{column_name}` = :value_to_replace"
        params = {"new_value": new_value, "value_to_replace": value_to_replace}
        self._execute(query, params)

    def delete_table(self, table_name):
        self._execute(f"DROP TABLE `{table_name}`")

    def strip_left(self, table_name, column_name, value_to_strip):
        query = f"UPDATE `{table_name}` SET `{column_name}` = SUBSTRING(`{column_name}`, LOCATE(:value_to_strip, `{column_name}`) + {len(value_to_strip)})"
        params = {"value_to_strip": value_to_strip}
        self._execute(query, params)

    def strip_right(self, table_name, column_name, value_to_strip):
        query = f"UPDATE `{table_name}` SET `{column_name}` = SUBSTRING(`{column_name}`, 1, LENGTH(`{column_name}`) - LOCATE(:value_to_strip, REVERSE(`{column_name}`)) - LENGTH(:value_to_strip) + 1)"
        params = {"value_to_strip": value_to_strip}
        self._execute(query, params)

    def replace_string(self, table_name, column_name, old_string, new_string):
        query = f"UPDATE `{table_name}` SET `{column_name}` = REPLACE(`{column_name}`, '{old_string}', '{new_string}')"
        self._execute(query)

    def replace_nulls(self, table_name, column_name, value):
        query = f"UPDATE `{table_name}` SET `{column_name}` = :value WHERE `{column_name}` IS NULL"
        params = {"value": value}
        self._execute(query, params)

    def rename_column(self, table_name, old_column_name, new_column_name, new_column_type: type | None = None):
        LOGGER.debug(f"Renaming column '{old_column_name}' in table '{table_name}' to '{new_column_name}'")
        if new_column_type is not None:
            sql_type = self._python_to_sql_type(new_column_type)
        else:
            sql_type = self._detect_column_sql_type(table_name, old_column_name)

        query = f"ALTER TABLE `{table_name}` CHANGE `{old_column_name}` `{new_column_name}` {sql_type}"
        self._execute(query)

    def change_type(self, table_name, column_name, new_column_type):
        query = f"ALTER TABLE `{table_name}` MODIFY `{column_name}` {self._python_to_sql_type(new_column_type)}"
        self._execute(query)
    
    def replace_yes_null(self, table_name, column_name):
        self.replace_nulls(table_name=table_name, column_name=column_name, value=0)
        self.replace_values(table_name=table_name, column_name=column_name, value_to_replace="yes", new_value=1)
        self.change_type(table_name=table_name, column_name=column_name, new_column_type=bool)

    def replace_TRUE_FALSE(self, table_name, column_name):
        self.replace_values(table_name=table_name, column_name=column_name, value_to_replace="TRUE", new_value=1)
        self.replace_values(table_name=table_name, column_name=column_name, value_to_replace="FALSE", new_value=0)
        self.change_type(table_name=table_name, column_name=column_name, new_column_type=bool)
