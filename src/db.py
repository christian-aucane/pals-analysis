import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from config import LOGGER

# TODO : ajouter la gestion des transactions

class DatabaseConnexion:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = None
        self.connection = None
        self._connect()

    def load_df_as_table(self, df, table_name, if_exists="replace"):
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)

    def get_df_from_query(self, query):
        return pd.read_sql(query, self.engine)
    
    def _execute(self, query, params=None):
        # TODO : ajouter optimisation du nb de connexions et de requetes
        display = query[:]
        if params is not None:
            for k, v in params.items():
                display = display.replace(f":{k}", f"'{v}'")
        LOGGER.debug(f"Executing query : {display}")
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query), params)
                connection.commit()
        except OperationalError as e:
            print(e)

    def delete_columns(self, table_name, column_names):
        with self.engine.connect() as connection:
            query = f"ALTER TABLE `{table_name}` " + ", ".join([f"DROP COLUMN {col}" for col in column_names])
            self._execute(query)

    def replace_values(self, table_name, column_name, value_to_replace, new_value):
        query = f"UPDATE `{table_name}` SET `{column_name}` = :new_value WHERE `{column_name}` = :value_to_replace"
        params = {"new_value": new_value, "value_to_replace": value_to_replace}
        self._execute(query, params)

    def replace_nulls(self, table_name, column_name, value):
        query = f"UPDATE `{table_name}` SET `{column_name}` = :value WHERE `{column_name}` IS NULL"
        params = {"value": value}
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

    def rename_column(self, table_name, old_column_name, new_column_name, new_column_type=None):
        if new_column_type is None:
            # TODO : récupérer le type dunamiquement a la place de str !!
            new_column_type = str
            ...
        query = f"ALTER TABLE `{table_name}` CHANGE `{old_column_name}` `{new_column_name}` {self._sql_type(new_column_type)}"
        self._execute(query)

    def change_type(self, table_name, column_name, new_column_type):
        query = f"ALTER TABLE `{table_name}` MODIFY `{column_name}` {self._sql_type(new_column_type)}"
        self._execute(query)

    @staticmethod
    def _sql_type(column_type):
        python_to_sql = {bool: "TINYINT(1)", int: "INT", float: "FLOAT", str: "VARCHAR(255)"}
        try:
            return python_to_sql[column_type]
        except KeyError:
            raise ValueError(f"Unknown column type : {column_type} - Only {' '.join(map(str, python_to_sql.keys()))} are supported")
        
    def _connect(self):
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')
        self.connection = self.engine.connect()
        self._execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self._execute(f"USE {self.database}")

    def _close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self._close()

if __name__ == "__main__":
    db = DatabaseConnexion("root", "root", "localhost", "test")
    df = pd.DataFrame.from_dict({"a": [1, 2, 3], "b": [4, 5, 6]})
    db.load_df_as_table(df, "test_table")
    print(db.get_df_from_query("SELECT * FROM test_table"))
