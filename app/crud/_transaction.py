from app import model
from app.crud._crud import Crud


class CrudTransaction(
    Crud[
        model.TransactionInput,
        model.TransactionDatabase,
        model.TransactionOutput,
        model.TransactionUpdate,
    ]
):
    pass


transaction = CrudTransaction(model.TransactionDatabase)
