from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud, model


def test_create_payee(client: TestClient):
    input_json = {"name": "Landlord"}
    response = client.post("/payee/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == 1
    assert content["name"] == input_json["name"]
    assert content["expenditure"] == 0


def test_create_payee_incomplete(client: TestClient):
    input_json = {}  # type: ignore
    response = client.post("/payee/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_payee_invalid(client: TestClient):
    input_json = {"name": None}
    response = client.post("/payee/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicated(client: TestClient):
    input_json = {"name": "Landlord"}
    client.post("/payee/", json=input_json)
    response = client.post("/payee/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content["detail"] == "Name already registered"


def test_read_payee(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    response = client.get(f"/payee/{row.id}")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["expenditure"] == 0


def test_read_payee_invalid(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    invalid_id = row.id + 1
    response = client.get(f"/payee/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Payee not found"


def test_read_many_payees(session: Session, client: TestClient):
    input_0 = model.PayeeInput(name="Landlord")
    row_0 = crud.payee.create(session, input_0)

    input_1 = model.PayeeInput(name="Supermarket")
    row_1 = crud.payee.create(session, input_1)

    response = client.get("/payee/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert content[0]["id"] == row_0.id
    assert content[0]["name"] == input_0.name
    assert content[0]["expenditure"] == 0

    assert content[1]["id"] == row_1.id
    assert content[1]["name"] == input_1.name
    assert content[1]["expenditure"] == 0


def test_read_many_payees_empty(client: TestClient):
    response = client.get("/payee/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content == []


def test_update_payee(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    update_json = {"name": "Supermarket"}
    response = client.put(f"/payee/{row.id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == update_json["name"]
    assert content["expenditure"] == 0

    assert content["name"] != input_.name


def test_update_payee_invalid(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    invalid_id = row.id + 1
    update_json = {"name": "Supermarket"}
    response = client.put(f"/payee/{invalid_id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Payee not found"


def test_delete_payee(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    response = client.delete(f"/payee/{row.id}")
    content = response.json()

    in_database = crud.payee.is_in_database(session, row.id)

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["expenditure"] == 0

    assert in_database is False


def test_delete_payee_invalid(session: Session, client: TestClient):
    input_ = model.PayeeInput(name="Landlord")
    row = crud.payee.create(session, input_)

    invalid_id = row.id + 1
    response = client.delete(f"/payee/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Payee not found"
