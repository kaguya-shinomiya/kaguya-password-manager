import os
from pathlib import Path

from kaguya.db_utils import create_connection, create_table, insert, sql_commands


def test_create_connection_creates_dbfile():
    test_db_file = Path(__file__).parent / "data" / "testcreationdb"
    conn = create_connection(test_db_file)  # create a connection
    conn.close()
    assert os.path.isfile(test_db_file)
    os.remove(test_db_file)


def test_create_table(db_conn):
    create_table(db_conn, sql_commands.create_credentials_table)
    c = db_conn.cursor()
    c.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='credentials';
    """
    )
    assert c.fetchone()


def test_insert_row(db_conn, insert_into_dummy_sql):
    insert(db_conn, insert_into_dummy_sql, ("doge", "password"))
    c = db_conn.cursor()
    c.execute(
        """
        SELECT * FROM dummy
        WHERE username = 'doge';
     """
    )
    assert c.fetchone() == (1, "doge", "password")
