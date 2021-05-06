import sqlite3
from pathlib import Path
from typing import Dict, Tuple

from loguru import logger


class EntityManager:
    def __init__(self, db_file: Path):
        self.conn = self._create_connection(db_file)

    @classmethod
    def _create_connection(cls, db_file: Path) -> sqlite3.Connection:
        """
        Create database connection to SQLite db.

        :param db_file: absolute path to db file
        :returns: Connection object
        """
        conn = sqlite3.connect(db_file)
        logger.info("connected to database")
        return conn

    def create_table(self, create_table_sql: str) -> None:
        """create table using `create_table_sql`"""
        c = self.conn.cursor()
        c.execute(create_table_sql)
        logger.info("created credentials table")

    def insert_chika(
        self,
        name: str,
        username: str,
        password: str,
    ) -> Tuple:
        """inserts a new set of credentials"""
        c = self.conn.cursor()
        c.execute(SqlCommands.insert_one_blob, [name, username, password])
        c.execute(SqlCommands.query_one_blob, [name])  # get the entire object
        return c.fetchone()

    def update_chika(
        self,
        chika_name: str,
        **params: Dict,
    ) -> Tuple:
        """updates one set of credentials"""
        cols_to_set = ", ".join([f"{k} = '{v}'" for (k, v) in params.items()])
        update_chika_sql = f"""
            UPDATE credentials
            SET {cols_to_set}
            WHERE name = '{chika_name}';
            """
        logger.debug(update_chika_sql)
        c = self.conn.cursor()
        c.execute(update_chika_sql)
        c.execute(SqlCommands.query_one_blob, [params.get("name", chika_name)])
        return c.fetchone()


class SqlCommands:
    create_credentials_table = """
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """

    insert_one_blob = """
        INSERT INTO credentials(name, username, password)
        VALUES(?,?,?);
        """

    query_one_blob = """
        SELECT name, username, password FROM credentials
        WHERE name = ?;
        """
