import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.engine.create import URL
from sqlmodel.pool import StaticPool

from app.config import settings
from app.dependency import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    database_url = URL.create(
        drivername="postgresql",
        username=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_FQDN,
        port=5432,
        database="test",
    )
    engine = create_engine(database_url, poolclass=StaticPool)

    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
