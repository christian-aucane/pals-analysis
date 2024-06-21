import pandas as pd


class _DataframeManager:
    def __init__(self, db_connexion):
        self._db_connexion = db_connexion

    def get_df_from_query(self, query: str):
        return pd.read_sql(query, self._db_connexion.engine)
    
    def load_df_as_table(self, df: pd.DataFrame,
                         table_name: str,
                         if_exists: str = "replace"):  # "fail", "replace", "append"
        df.to_sql(table_name,
                  self._db_connexion.engine,
                  if_exists=if_exists,
                  index=False)
