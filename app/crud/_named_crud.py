import abc
from typing import Optional, TypeVar

from sqlmodel import Session, select

from app import model
from app.crud._crud import Crud
from app.model import NamedModelDatabase, NamedModelInput, NamedModelOutput, NamedModelUpdate

AnyNamedModelInput = TypeVar("AnyNamedModelInput", bound=NamedModelInput)
AnyNamedModelDatabase = TypeVar("AnyNamedModelDatabase", bound=NamedModelDatabase)
AnyNamedModelOutput = TypeVar("AnyNamedModelOutput", bound=NamedModelOutput)
AnyNamedModelUpdate = TypeVar("AnyNamedModelUpdate", bound=NamedModelUpdate)


class NamedCrud(
    Crud[AnyNamedModelInput, AnyNamedModelDatabase, AnyNamedModelOutput, AnyNamedModelUpdate],
    abc.ABC,
):
    def get_by_name(self, session: Session, name: str) -> Optional[AnyNamedModelDatabase]:
        statement = select(self.model_database).where(self.model_database.name == name)
        result = session.exec(statement)
        row = result.first()

        return row

    @abc.abstractmethod
    def get_full(self, session: Session, id_: int):
        pass

    def _get_full(self, session: Session, id_: int, *args):
        statement = (
            select(self.model_database.id, self.model_database.name, *args)
            .join(model.TransactionDatabase, isouter=True)
            .where(self.model_database.id == id_)
            .group_by(self.model_database.id)
        )
        result = session.exec(statement)
        row = result.first()

        return row

    @abc.abstractmethod
    def get_many_full(self, session: Session, skip: int, limit: int):
        pass

    def _get_many_full(self, session: Session, skip: int, limit: int, *args):
        statement = (
            select(self.model_database.id, self.model_database.name, *args)
            .join(model.TransactionDatabase, isouter=True)
            .group_by(self.model_database.id)
            .order_by(self.model_database.id)
            .offset(skip)
            .limit(limit)
        )
        result = session.exec(statement)
        rows = result.all()

        return rows
