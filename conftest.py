import os
import sqlite3
from pathlib import Path

import pytest

test_db_file = Path(__file__).parent / "tests" / "data" / "testsqlite"


@pytest.fixture(scope="session", autouse=True)
def db_conn():
    conn = sqlite3.connect(test_db_file)
    yield conn
    conn.close()  # runs after all tests
    os.remove(test_db_file)
