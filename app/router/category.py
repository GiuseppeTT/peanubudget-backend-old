from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app import crud, model
from app.dependency import ExistentIdChecker, get_session

router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

check_existent_id = ExistentIdChecker("Category", crud.category)


@router.post("/", response_model=model.CategoryOutput)
def create(*, session: Session = Depends(get_session), input_: model.CategoryInput):
    try:
        row = crud.category.create(session, input_)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name already registered"
        ) from exc

    full_row = crud.category.get_full(session, row.id)

    return full_row


@router.get("/{id_}", response_model=model.CategoryOutput)
def read(*, session: Session = Depends(get_session), id_: int = Depends(check_existent_id)):
    full_row = crud.category.get_full(session, id_)

    return full_row


@router.get("/", response_model=list[model.CategoryOutput])
def read_many(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    full_rows = crud.category.get_many_full(session, skip, limit)

    return full_rows


@router.put("/{id_}", response_model=model.CategoryOutput)
def update(
    *,
    session: Session = Depends(get_session),
    id_: int = Depends(check_existent_id),
    update_: model.CategoryUpdate
):
    row = crud.category.update(session, id_, update_)
    full_row = crud.category.get_full(session, row.id)

    return full_row


@router.delete("/{id_}", response_model=model.CategoryOutput)
def delete(*, session: Session = Depends(get_session), id_: int = Depends(check_existent_id)):
    full_row = crud.category.get_full(session, id_)
    crud.category.delete(session, id_)

    return full_row
