import datetime
import os
from pathlib import Path
from typing import List

from loguru import logger
from sqlalchemy import Column, DateTime, Integer, String, create_engine, delete, select
from sqlalchemy.orm import Session, declarative_base

DB_FILE = Path(__file__).parent / "data" / "kaguya.db"
Base = declarative_base()


class Chika(
    Base
):  # inherting from Base allows this table to be created automatically when create_all is called later
    __tablename__ = "chikas"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    domain = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"Chika(id={self.id!r} name={self.name!r} username={self.username!r} password={self.password!r} domain={self.domain!r})"


class DbUtils:
    def __init__(self, db_file: Path):
        engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
        self.session = Session(engine)

        Base.metadata.create_all(engine)

    def create_chika(
        self,
        domain: str = None,
        *args,
        name: str,
        username: str,
        password: str,
    ):
        new_chika = Chika(
            name=name,
            password=password,
            username=username,
            domain=domain,
        )
        self.session.add(new_chika)
        self.session.flush()

    def select_chika_by_id(self, id: int) -> Chika:
        chika = self.session.execute(select(Chika).filter_by(id=id)).scalar_one()
        return chika

    def select_chika_by_name(self, name: str) -> List[Chika]:
        result = self.session.execute(
            select(Chika).filter_by(name=name).order_by(Chika.created_at)
        )
        return result.scalars().all()

    def get_all_chikas(self) -> List[Chika]:
        result = self.session.execute(select(Chika).order_by(Chika.created_at))
        return result.scalars().all()

    def delete_chika(self, id: int):
        self.session.execute(delete(Chika).where(Chika.id == id))

    def update_chika(self, id, **fields):
        chika = self.session.execute(select(Chika).filter_by(id=id)).scalar_one()
        for field, field_value in fields.items():
            setattr(chika, field, field_value)
        self.session.flush()

    def close_session(self):
        self.session.close()


if __name__ == "__main__":
    db_utils = DbUtils(DB_FILE)
    db_utils.create_chika(
        name="chikabook",
        username="chika",
        password="password",
    )
    db_utils.create_chika(
        name="chikabook",
        username="kaguya",
        password="password",
    )
    logger.info(db_utils.select_chika_by_id(1))
    logger.info(db_utils.select_chika_by_name("chikabook"))
    logger.info(db_utils.get_all_chikas())
    db_utils.delete_chika(1)  # deletes chika's entry
    logger.info(db_utils.select_chika_by_name("chikabook"))
    db_utils.update_chika(
        2, name="kei", school="Shuchi'in Academy Shuchiin Academy"
    )  # change kaguya's entry to kei, irrelevant school field is ignored
    logger.info(db_utils.select_chika_by_id(2))

    db_utils.close_session()  # close session
    os.remove(DB_FILE)  # teardown
    logger.info("db deleted")
