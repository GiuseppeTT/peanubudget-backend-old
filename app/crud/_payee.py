from sqlmodel import Session, func

from app import model
from app.crud._named_crud import NamedCrud


class CrudPayee(
    NamedCrud[model.PayeeInput, model.PayeeDatabase, model.PayeeOutput, model.PayeeUpdate]
):
    def get_full(self, session: Session, id_: int):
        expenditure = func.coalesce(func.sum(model.TransactionDatabase.value), 0).label(
            "expenditure"
        )
        row = self._get_full(session, id_, expenditure)

        return row

    def get_many_full(self, session: Session, skip: int, limit: int):
        expenditure = func.coalesce(func.sum(model.TransactionDatabase.value), 0).label(
            "expenditure"
        )
        rows = self._get_many_full(session, skip, limit, expenditure)

        return rows


payee = CrudPayee(model.PayeeDatabase)
