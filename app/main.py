from fastapi import FastAPI

from app.database import create_database_and_tables
from app.router import account, category, payee, transaction

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_database_and_tables()


app.include_router(account.router)
app.include_router(payee.router)
app.include_router(category.router)
app.include_router(transaction.router)
