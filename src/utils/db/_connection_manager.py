from functools import reduce
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pandas as pd


LOGGER = logging.getLogger("CONNECTION")


class _DbConnexionManager:
    def __init__(self, user: str, password: str, host: str, database: str):
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
    def _connect(self):  # TODO : ajouter gestion d'erreur
        LOGGER.info("CONNECTING TO DATABASE...")
        db_uri = f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
        self.engine = create_engine(db_uri)
        self.connection = self.engine.connect()
        self.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.execute(f"USE {self.database}")
        LOGGER.info("CONNECTED !\n")

    def _close(self):
        LOGGER.info("CLOSING CONNECTION ...")
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.engine:
            self.engine.dispose()
            self.engine = None
        LOGGER.info("CONNECTION CLOSED !\n")

    # PUBLIC METHOD
    def execute(self, query: str, params: dict = {}):
        # TODO : add optimization of nb of connections and queries
        formatted_query = reduce(lambda q, kv: q.replace(f":{kv[0]}",
                                                         f"'{kv[1]}'"),
                                                         params.items(),
                                                         query)
        LOGGER.debug(f"Executing query : {formatted_query}")
        try:
            self.connection.execute(text(query), params)
            self.connection.commit()
        except OperationalError as e:
            LOGGER.error(e)
