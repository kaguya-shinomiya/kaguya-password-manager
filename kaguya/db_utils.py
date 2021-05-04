import sqlite3
from pathlib import Path

from loguru import logger


def create_connection(db_file: Path) -> sqlite3.Connection:
    """create database connection to SQLite db"""
    conn = None  # initialize empty var here
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        logger.error(repr(e))
    return conn


def create_table(conn: sqlite3.Connection, create_table_sql: str):
    """create table using `create_table_sql`"""
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        logger.error(repr(e))


create_credentials_table_sql = """
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
"""
