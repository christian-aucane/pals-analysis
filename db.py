import pandas as pd
from sqlalchemy import create_engine, text


class DataframeToDatabaseLoader:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = None
        self._connect()
    
    def load(self, df, table_name, if_exists="replace"):
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)

    def _connect(self):
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')
        with self.engine.connect() as connection:

            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database}"))
            connection.execute(text(f"USE {self.database}"))

    def _close(self):
        if self.engine:
            self.engine.dispose()

    def __del__(self):
        self._close()


if __name__ == "__main__":

    loader = DataframeToDatabaseLoader("root", "root", "localhost", "test")
    df = pd.DataFrame.from_dict({"a": [1, 2, 3], "b": [4, 5, 6]})
    loader.load(df, "test_table")
