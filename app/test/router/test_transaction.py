from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud, model


def test_create_transaction(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_json = {
        "date_time": "2020-03-04T18:52:50.637635",
        "account_id": account_row.id,
        "payee_id": payee_row.id,
        "category_id": category_row.id,
        "value": 1_000,
        "comment": "Rent payment",
    }
    response = client.post("/transaction/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == 1
    assert content["date_time"] == input_json["date_time"]
    assert content["account_id"] == account_row.id
    assert content["payee_id"] == payee_row.id
    assert content["category_id"] == category_row.id
    assert content["value"] == input_json["value"]
    assert content["comment"] == input_json["comment"]


def test_create_transaction_untracked(client: TestClient):
    input_json = {
        "date_time": "2020-03-04T18:52:50.637635",
        "account_id": None,
        "payee_id": None,
        "category_id": None,
        "value": 111,
        "comment": "Random stuff",
    }
    response = client.post("/transaction/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == 1
    assert content["date_time"] == input_json["date_time"]
    assert content["account_id"] == input_json["account_id"]
    assert content["payee_id"] == input_json["payee_id"]
    assert content["category_id"] == input_json["category_id"]
    assert content["value"] == input_json["value"]
    assert content["comment"] == input_json["comment"]


def test_create_transaction_incomplete(client: TestClient):
    input_json = {}  # type: ignore
    response = client.post("/transaction/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_transaction_invalid(client: TestClient):
    input_json = {"value": None}
    response = client.post("/transaction/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_transaction_invalid_account(client: TestClient):
    input_json = {
        "date_time": "2020-03-04T18:52:50.637635",
        "account_id": 1,
        "payee_id": None,
        "category_id": None,
        "value": 1_000,
        "comment": "Rent payment",
    }
    response = client.post("/transaction/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Account not found"


def test_create_transaction_invalid_payee(client: TestClient):
    input_json = {
        "date_time": "2020-03-04T18:52:50.637635",
        "account_id": None,
        "payee_id": 1,
        "category_id": None,
        "value": 1_000,
        "comment": "Rent payment",
    }
    response = client.post("/transaction/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Payee not found"


def test_create_transaction_invalid_category(client: TestClient):
    input_json = {
        "date_time": "2020-03-04T18:52:50.637635",
        "account_id": None,
        "payee_id": None,
        "category_id": 1,
        "value": 1_000,
        "comment": "Rent payment",
    }
    response = client.post("/transaction/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Category not found"


def test_read_transaction(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    response = client.get(f"/transaction/{row.id}")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["date_time"] == row.date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["account_id"] == account_row.id
    assert content["payee_id"] == payee_row.id
    assert content["category_id"] == category_row.id
    assert content["value"] == row.value
    assert content["comment"] == row.comment


def test_read_transaction_invalid(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    invalid_id = row.id + 1
    response = client.get(f"/transaction/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Transaction not found"


def test_read_many_transactions(session: Session, client: TestClient):
    account_input_0 = model.AccountInput(name="Checking")
    account_row_0 = crud.account.create(session, account_input_0)

    payee_input_0 = model.PayeeInput(name="Landlord")
    payee_row_0 = crud.payee.create(session, payee_input_0)

    category_input_0 = model.CategoryInput(name="Rent", budget=1_000)
    category_row_0 = crud.category.create(session, category_input_0)

    input_0 = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row_0.id,
        payee_id=payee_row_0.id,
        category_id=category_row_0.id,
        value=1_000,
        comment="Rent payment",
    )
    row_0 = crud.transaction.create(session, input_0)

    account_input_1 = model.AccountInput(name="Savings")
    account_row_1 = crud.account.create(session, account_input_1)

    payee_input_1 = model.PayeeInput(name="Supermarket")
    payee_row_1 = crud.payee.create(session, payee_input_1)

    category_input_1 = model.CategoryInput(name="Food", budget=500)
    category_row_1 = crud.category.create(session, category_input_1)

    input_1 = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row_1.id,
        payee_id=payee_row_1.id,
        category_id=category_row_1.id,
        value=100,
        comment=None,
    )
    row_1 = crud.transaction.create(session, input_1)

    response = client.get("/transaction/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert content[0]["id"] == row_0.id
    assert content[0]["date_time"] == row_0.date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content[0]["account_id"] == account_row_0.id
    assert content[0]["payee_id"] == payee_row_0.id
    assert content[0]["category_id"] == category_row_0.id
    assert content[0]["value"] == row_0.value
    assert content[0]["comment"] == row_0.comment

    assert content[1]["id"] == row_1.id
    assert content[1]["date_time"] == row_1.date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content[1]["account_id"] == account_row_1.id
    assert content[1]["payee_id"] == payee_row_1.id
    assert content[1]["category_id"] == category_row_1.id
    assert content[1]["value"] == row_1.value
    assert content[1]["comment"] == row_1.comment


def test_read_many_transactions_empty(client: TestClient):
    response = client.get("/transaction/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content == []


def test_update_transaction(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    update_json = {"value": 42}
    response = client.put(f"/transaction/{row.id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["date_time"] == row.date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["account_id"] == account_row.id
    assert content["payee_id"] == payee_row.id
    assert content["category_id"] == category_row.id
    assert content["value"] == row.value
    assert content["comment"] == row.comment

    assert content["value"] != input_.value


def test_update_transaction_invalid(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    invalid_id = row.id + 1
    update_json = {"value": 42}
    response = client.put(f"/transaction/{invalid_id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Transaction not found"


def test_delete_transaction(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    response = client.delete(f"/transaction/{row.id}")
    content = response.json()

    in_database = crud.transaction.is_in_database(session, row.id)

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["date_time"] == row.date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["account_id"] == account_row.id
    assert content["payee_id"] == payee_row.id
    assert content["category_id"] == category_row.id
    assert content["value"] == row.value
    assert content["comment"] == row.comment

    assert in_database is False


def test_delete_transaction_invalid(session: Session, client: TestClient):
    account_input = model.AccountInput(name="Checking")
    account_row = crud.account.create(session, account_input)

    payee_input = model.PayeeInput(name="Landlord")
    payee_row = crud.payee.create(session, payee_input)

    category_input = model.CategoryInput(name="Rent", budget=1_000)
    category_row = crud.category.create(session, category_input)

    input_ = model.TransactionInput(
        date_time=datetime.now(),
        account_id=account_row.id,
        payee_id=payee_row.id,
        category_id=category_row.id,
        value=1_000,
        comment="Rent payment",
    )
    row = crud.transaction.create(session, input_)

    invalid_id = row.id + 1
    response = client.delete(f"/transaction/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Transaction not found"
