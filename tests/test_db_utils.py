import os
from pathlib import Path

from kaguya.db_utils import EntityManager, SqlCommands


def test_create_connection_creates_dbfile():
    test_db_file = Path(__file__).parent / "data" / "testcreationdb"
    conn = EntityManager._create_connection(test_db_file)  # create a connection
    conn.close()
    assert os.path.isfile(test_db_file)
    os.remove(test_db_file)


def test_create_table(em):
    em.create_table(
        """
        CREATE TABLE IF NOT EXISTS dummy (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        """
    )
    c = em.conn.cursor()
    c.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='dummy';
    """
    )

    assert c.fetchone()

    c.execute("DROP TABLE dummy;")


def test_insert_chika(em):
    name, username, password = "dogehouse", "doge", "password"
    new_chika = em.insert_chika(name, username, password)

    assert new_chika == ("dogehouse", "doge", "password")


def test_update_chika(em):
    name, username, password = "cheemshouse", "cheems", "password"
    em.insert_chika(name, username, password)

    c = em.conn.cursor()
    c.execute(SqlCommands.query_one_blob, [])

    new_chika = em.update_chika("cheemshouse", name="cheemsburger", password="123456")

    assert new_chika == ("cheemsburger", "cheems", "123456")
