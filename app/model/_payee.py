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


class PayeeInput(NamedModelInput):
    pass


class PayeeDatabase(NamedModelDatabase, table=True):
    __tablename__ = "payee"

    transactions: list["TransactionDatabase"] = Relationship(back_populates="payee")


class PayeeOutput(NamedModelOutput):
    expenditure: float


class PayeeUpdate(NamedModelUpdate):
    pass
