from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud, model


def test_create_category(client: TestClient):
    input_json = {"name": "Rent", "budget": 1_000}
    response = client.post("/category/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == 1
    assert content["name"] == input_json["name"]
    assert content["budget"] == input_json["budget"]
    assert content["expenditure"] == 0
    assert content["available"] == input_json["budget"] + 0  # type: ignore


def test_create_category_incomplete(client: TestClient):
    input_json = {}  # type: ignore
    response = client.post("/category/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_category_invalid(client: TestClient):
    input_json = {"name": None}
    response = client.post("/category/", json=input_json)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicated(client: TestClient):
    input_json = {"name": "Rent", "budget": 1_000}
    client.post("/category/", json=input_json)
    response = client.post("/category/", json=input_json)
    content = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert content["detail"] == "Name already registered"


def test_read_category(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    response = client.get(f"/category/{row.id}")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["budget"] == input_.budget
    assert content["expenditure"] == 0
    assert content["available"] == input_.budget + 0


def test_read_category_invalid(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    invalid_id = row.id + 1
    response = client.get(f"/category/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Category not found"


def test_read_many_categorys(session: Session, client: TestClient):
    input_0 = model.CategoryInput(name="Rent", budget=1_000)
    row_0 = crud.category.create(session, input_0)

    input_1 = model.CategoryInput(name="Food", budget=500)
    row_1 = crud.category.create(session, input_1)

    response = client.get("/category/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert content[0]["id"] == row_0.id
    assert content[0]["name"] == input_0.name
    assert content[0]["budget"] == input_0.budget
    assert content[0]["expenditure"] == 0
    assert content[0]["available"] == input_0.budget + 0

    assert content[1]["id"] == row_1.id
    assert content[1]["name"] == input_1.name
    assert content[1]["budget"] == input_1.budget
    assert content[1]["expenditure"] == 0
    assert content[1]["available"] == input_1.budget + 0


def test_read_many_categorys_empty(client: TestClient):
    response = client.get("/category/")
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content == []


def test_update_category(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    update_json = {"name": "Food", "budget": 500}
    response = client.put(f"/category/{row.id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == update_json["name"]
    assert content["budget"] == update_json["budget"]
    assert content["expenditure"] == 0
    assert content["available"] == update_json["budget"] + 0  # type: ignore

    assert content["name"] != input_.name
    assert content["budget"] != input_.budget
    # assert content["expenditure"] != ...
    assert content["available"] != input_.budget + 0


def test_update_category_invalid(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    invalid_id = row.id + 1
    update_json = {"name": "Food", "budget": 500}
    response = client.put(f"/category/{invalid_id}", json=update_json)
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Category not found"


def test_delete_category(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    response = client.delete(f"/category/{row.id}")
    content = response.json()

    in_database = crud.category.is_in_database(session, row.id)

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == row.id
    assert content["name"] == input_.name
    assert content["budget"] == input_.budget
    assert content["expenditure"] == 0
    assert content["available"] == input_.budget + 0

    assert in_database is False


def test_delete_category_invalid(session: Session, client: TestClient):
    input_ = model.CategoryInput(name="Rent", budget=1_000)
    row = crud.category.create(session, input_)

    invalid_id = row.id + 1
    response = client.delete(f"/category/{invalid_id}")
    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content["detail"] == "Category not found"
