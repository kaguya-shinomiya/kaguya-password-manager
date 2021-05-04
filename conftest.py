import os
import sqlite3
from pathlib import Path

import pytest

test_db_file = Path(__file__).parent / "tests" / "data" / "testsqlite"


@pytest.fixture(scope="session", autouse=True)
def db_conn():
    conn = sqlite3.connect(test_db_file)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS dummy (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """
    )
    yield conn
    conn.close()  # runs after all tests
    os.remove(test_db_file)


@pytest.fixture(scope="module")
def insert_into_dummy_sql():
    return "INSERT INTO dummy(username, password) VALUES(?,?);"
