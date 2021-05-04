import os
from pathlib import Path

from kaguya.db_utils import (
    create_connection,
    create_credentials_table_sql,
    create_table,
)


def test_create_connection_creates_dbfile():
    test_db_file = Path(__file__).parent / "data" / "testcreationdb"
    conn = create_connection(test_db_file)  # create a connection
    conn.close()
    assert os.path.isfile(test_db_file)
    os.remove(test_db_file)


def test_create_credentials_table(db_conn):
    create_table(db_conn, create_credentials_table_sql)
    c = db_conn.cursor()
    c.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='credentials';
    """
    )
    assert c.fetchone()
