import sqlite3
from pathlib import Path
from string import Template
from typing import Iterable

from loguru import logger


def create_connection(db_file: Path) -> sqlite3.Connection:
    """create database connection to SQLite db"""
    conn = None  # initialize empty var here
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        logger.error(repr(e))
    return conn


def create_table(conn: sqlite3.Connection, create_table_sql: str) -> None:
    """create table using `create_table_sql`"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        logger.error(repr(e))


def insert(conn: sqlite3.Connection, insert_sql: str, vals: Iterable) -> None:
    """insert a row into some table"""
    try:
        c = conn.cursor()
        c.execute(insert_sql, vals)
    except sqlite3.Error as e:
        logger.error(repr(e))


class sql_commands:
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

    update_one_blob: Template = Template(
        """
        UPDATE credentials
        SET name = ?,
            username = ?,
            password = ?
        WHERE name = ?;
        """
    )
