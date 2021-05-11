import datetime
from enum import unique
import os
from pathlib import Path
from typing import List

from loguru import logger
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    delete,
    exc,
    select,
)
from sqlalchemy.orm import Session, declarative_base, session

DB_FILE = Path(__file__).parent / "data" / "testmasteruser.db"
Base = declarative_base()


class Account(
    Base
):  # inherting from Base allows this table to be created automatically when create_all is called later
    __tablename__ = "master"

    id = Column(Integer, primary_key=True)
    masteruser = Column(String, nullable=False, unique=True)
    masterpass = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"master(id={self.id!r} masteruser={self.masteruser!r} masterpass={self.masterpass!r})"


class MasterDbUtils:
    def __init__(self, db_file: Path):
        engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
        self.session = Session(engine)

        Base.metadata.create_all(engine)

    def create_account(
        self,
        masteruser: str,
        masterpass: str,
    ):
        new_user = Account(
            masteruser=masteruser,
            masterpass=masterpass,
        )
        self.session.add(new_user)
        try:
            self.session.commit()
            return True
        except exc.IntegrityError:
            print("Username has been taken, please try again.")
            self.session.rollback()

    def select_account_by_id(self, id: int) -> Account:
        account = self.session.execute(select(Account).filter_by(id=id)).scalar_one()
        return account

    def select_account_by_masteruser(self, masteruser: str) -> List[Account]:
        result = self.session.execute(
            select(Account)
            .filter_by(masteruser=masteruser)
            .order_by(Account.created_at)
        )
        return result.scalars().all()

    def get_all_accounts(self) -> List[Account]:
        result = self.session.execute(select(Account).order_by(Account.created_at))
        return result.scalars().all()

    def delete_account(self, id: int):
        self.session.execute(delete(Account).where(Account.id == id))

    def update_account(self, id, **fields):
        account = self.session.execute(select(Account).filter_by(id=id)).scalar_one()
        for field, field_value in fields.items():
            setattr(account, field, field_value)
        self.session.flush()
        self.session.commit()

    def close_session(self):
        self.session.close()


if __name__ == "__main__":
    master_db = MasterDbUtils(DB_FILE)
    master_db.create_account(
        masteruser="chicken",
        masterpass="nugget",
    )
    master_db.create_account(
        masteruser="gay",
        masterpass="fag",
    )
    logger.info(master_db.select_account_by_id(1))
    logger.info(master_db.get_all_accounts())
    master_db.delete_account(1)  # deletes chika's entry
    master_db.update_account(
        2, masteruser="straight", school="Shuchi'in Academy Shuchiin Academy"
    )  # change kaguya's entry to kei, irrelevant school field is ignored
    logger.info(master_db.select_account_by_id(2))

    master_db.close_session()  # close session
    os.remove(DB_FILE)  # teardown
    logger.info("db deleted")
