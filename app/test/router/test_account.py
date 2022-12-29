from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud, model


def test_create_account(client: TestClient):
    input_json = {"name": "Checking"}
    response = client.post("/account/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == 1
    assert content["name"] == input_json["name"]
    assert content["balance"] == 0


def test_create_account_incomplete(client: TestClient):
    input_json = {}  # type: ignore
    response = client.post("/account/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_account_invalid(client: TestClient):
    input_json = {"name": None}
    response = client.post("/account/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicated(client: TestClient):
    input_json = {"name": "Checking"}
    client.post("/account/", json=input_json)
    response = client.post("/account/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content["detail"] == "Name already registered"


def test_read_account(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    response = client.get(f"/account/{row.id}")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["balance"] == 0


def test_read_account_invalid(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    invalid_id = row.id + 1
    response = client.get(f"/account/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Account not found"


def test_read_many_accounts(session: Session, client: TestClient):
    input_0 = model.AccountInput(name="Checking")
    row_0 = crud.account.create(session, input_0)

    input_1 = model.AccountInput(name="Savings")
    row_1 = crud.account.create(session, input_1)

    response = client.get("/account/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert content[0]["id"] == row_0.id
    assert content[0]["name"] == input_0.name
    assert content[0]["balance"] == 0

    assert content[1]["id"] == row_1.id
    assert content[1]["name"] == input_1.name
    assert content[1]["balance"] == 0


def test_read_many_accounts_empty(client: TestClient):
    response = client.get("/account/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content == []


def test_update_account(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    update_json = {"name": "Savings"}
    response = client.put(f"/account/{row.id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == update_json["name"]
    assert content["balance"] == 0

    assert content["name"] != input_.name


def test_update_account_invalid(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    invalid_id = row.id + 1
    update_json = {"name": "Savings"}
    response = client.put(f"/account/{invalid_id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Account not found"


def test_delete_account(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    response = client.delete(f"/account/{row.id}")
    content = response.json()

    in_database = crud.account.is_in_database(session, row.id)

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["balance"] == 0

    assert in_database is False


def test_delete_account_invalid(session: Session, client: TestClient):
    input_ = model.AccountInput(name="Checking")
    row = crud.account.create(session, input_)

    invalid_id = row.id + 1
    response = client.delete(f"/account/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Account not found"
