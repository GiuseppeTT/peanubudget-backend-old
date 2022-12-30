from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.model._model import ModelDatabase, ModelInput, ModelOutput, ModelUpdate

if TYPE_CHECKING:
    from app.model._account import AccountDatabase
    from app.model._category import CategoryDatabase
    from app.model._payee import PayeeDatabase


class TransactionInput(ModelInput):
    date_time: datetime = Field(default_factory=datetime.now)
    account_id: Optional[int] = None
    payee_id: Optional[int] = None
    category_id: Optional[int] = None
    value: float
    comment: Optional[str] = None


class TransactionDatabase(ModelDatabase, table=True):
    __tablename__ = "transaction"

    date_time: datetime = Field(default_factory=datetime.now)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    payee_id: Optional[int] = Field(default=None, foreign_key="payee.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    value: float
    comment: Optional[str] = None

    account: Optional["AccountDatabase"] = Relationship(back_populates="transactions")
    payee: Optional["PayeeDatabase"] = Relationship(back_populates="transactions")
    category: Optional["CategoryDatabase"] = Relationship(back_populates="transactions")


class TransactionOutput(ModelOutput):
    date_time: datetime
    account_id: Optional[int] = None
    payee_id: Optional[int] = None
    category_id: Optional[int] = None
    value: float
    comment: Optional[str] = None


class TransactionUpdate(ModelUpdate):
    date_time: Optional[datetime] = None
    account_id: Optional[int] = None
    payee_id: Optional[int] = None
    category_id: Optional[int] = None
    value: Optional[float] = None
    comment: Optional[str] = None
