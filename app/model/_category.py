from typing import TYPE_CHECKING, Optional

from sqlmodel import Relationship

from app.model._named_model import (
    NamedModelDatabase,
    NamedModelInput,
    NamedModelOutput,
    NamedModelUpdate,
)

if TYPE_CHECKING:
    from app.model._transaction import TransactionDatabase


class CategoryInput(NamedModelInput):
    budget: float


class CategoryDatabase(NamedModelDatabase, table=True):
    __tablename__ = "category"

    budget: float

    transactions: list["TransactionDatabase"] = Relationship(back_populates="category")


class CategoryOutput(NamedModelOutput):
    budget: float
    expenditure: float
    available: float


class CategoryUpdate(NamedModelUpdate):
    budget: Optional[float] = None
