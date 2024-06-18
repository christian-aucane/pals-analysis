import pandas as pd
from sqlalchemy import create_engine, text


class DatabaseConnexion:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = None
        self._connect()
    
    def load_df_as_table(self, df, table_name, if_exists="replace"):
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)

    def get_df_from_query(self, query):
        return pd.read_sql(query, self.engine)

    def _connect(self):
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')
        with self.engine.connect() as connection:
            # TODO : fix this : DB is not created and raise an error if it doesn't exist
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database}"))
            connection.execute(text(f"USE {self.database}"))

    def _close(self):
        if self.engine:
            self.engine.dispose()

    def __del__(self):
        self._close()


if __name__ == "__main__":

    db = DatabaseConnexion("root", "root", "localhost", "test")
    df = pd.DataFrame.from_dict({"a": [1, 2, 3], "b": [4, 5, 6]})
    db.load_df_as_table(df, "test_table")
    print(db.get_df_from_query("SELECT * FROM test_table"))

