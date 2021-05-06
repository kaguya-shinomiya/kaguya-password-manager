import os
from pathlib import Path

import pytest

from kaguya.db_utils import EntityManager, SqlCommands


@pytest.fixture
def em(scope="session", autouse=True):
    test_db_file = Path(__file__).parent / "tests" / "data" / "testsqlite"
    em = EntityManager(test_db_file)
    em.create_table(SqlCommands.create_credentials_table)
    yield em
    # teardown
    em.conn.close()
    os.remove(test_db_file)
