from typing import TYPE_CHECKING

from sqlmodel import Relationship

from app.model._named_model import (
    NamedModelDatabase,
    NamedModelInput,
    NamedModelOutput,
    NamedModelUpdate,
)

if TYPE_CHECKING:
    from app.model._transaction import TransactionDatabase


class AccountInput(NamedModelInput):
    pass


class AccountDatabase(NamedModelDatabase, table=True):
    __tablename__ = "account"

    transactions: list["TransactionDatabase"] = Relationship(back_populates="account")


class AccountOutput(NamedModelOutput):
    balance: float


class AccountUpdate(NamedModelUpdate):
    pass
