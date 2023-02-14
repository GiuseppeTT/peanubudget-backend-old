from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_database_and_tables
from app.router import account, category, payee, transaction

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_database_and_tables()


app.include_router(account.router)
app.include_router(payee.router)
app.include_router(category.router)
app.include_router(transaction.router)
