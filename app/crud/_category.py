from sqlmodel import Session, func

from app import model
from app.crud._named_crud import NamedCrud


class CrudCategory(
    NamedCrud[
        model.CategoryInput, model.CategoryDatabase, model.CategoryOutput, model.CategoryUpdate
    ]
):
    def get_full(self, session: Session, id_: int):
        budget = self.model_database.budget
        expenditure = func.coalesce(func.sum(model.TransactionDatabase.value), 0).label(
            "expenditure"
        )
        available = (budget + expenditure).label("available")
        row = self._get_full(session, id_, budget, expenditure, available)

        return row

    def get_many_full(self, session: Session, skip: int, limit: int):
        budget = self.model_database.budget
        expenditure = func.coalesce(func.sum(model.TransactionDatabase.value), 0).label(
            "expenditure"
        )
        available = (budget + expenditure).label("available")
        rows = self._get_many_full(session, skip, limit, budget, expenditure, available)

        return rows


category = CrudCategory(model.CategoryDatabase)
