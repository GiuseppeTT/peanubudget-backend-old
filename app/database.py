from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.engine.create import URL

from app.config import settings

database_url = URL.create(
    drivername="postgresql",
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_FQDN,
    port=5432,
    database="prod",
)
engine = create_engine(database_url)


def create_database_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
