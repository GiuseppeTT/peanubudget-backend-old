import abc
from typing import Generic, Optional, Type, TypeVar

from sqlmodel import Session, select

from app.model import ModelDatabase, ModelInput, ModelOutput, ModelUpdate

AnyModelInput = TypeVar("AnyModelInput", bound=ModelInput)
AnyModelDatabase = TypeVar("AnyModelDatabase", bound=ModelDatabase)
AnyModelOutput = TypeVar("AnyModelOutput", bound=ModelOutput)
AnyModelUpdate = TypeVar("AnyModelUpdate", bound=ModelUpdate)


class Crud(Generic[AnyModelInput, AnyModelDatabase, AnyModelOutput, AnyModelUpdate], abc.ABC):
    def __init__(self, model_database: Type[AnyModelDatabase]):
        self.model_database = model_database

    def create(self, session: Session, input_: AnyModelInput) -> AnyModelDatabase:
        row = self.model_database(**input_.dict())
        session.add(row)
        session.commit()
        session.refresh(row)

        return row

    def get(self, session: Session, id_: int, none_ok: bool = True) -> Optional[AnyModelDatabase]:
        statement = select(self.model_database).where(self.model_database.id == id_)
        result = session.exec(statement)
        row = result.first()

        if none_ok:
            return row

        assert row is not None

        return row

    def get_many(self, session: Session, skip: int, limit: int) -> list[AnyModelDatabase]:
        statement = select(self.model_database).offset(skip).limit(limit)
        result = session.exec(statement)
        rows = result.all()

        return rows

    def update(self, session: Session, id_: int, update: AnyModelUpdate) -> AnyModelDatabase:
        row = self.get(session, id_)
        data_update = update.dict(exclude_unset=True)
        for key, value in data_update.items():
            setattr(row, key, value)
        session.add(row)
        session.commit()

        assert row is not None

        return row

    def delete(self, session: Session, id_: int) -> AnyModelDatabase:
        row = self.get(session, id_)
        session.delete(row)
        session.commit()

        assert row is not None

        return row

    def is_in_database(
        self, session: Session, id_: Optional[int] = None, none_ok: bool = False
    ) -> bool:
        if id_ is None:
            return none_ok

        row = self.get(session, id_, none_ok=True)
        in_database = row is not None

        return in_database
