from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud, model
from app.dependency import ExistentIdChecker, get_session

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

check_existent_id = ExistentIdChecker("Transaction", crud.transaction)


@router.post("/", response_model=model.TransactionOutput)
def create(*, session: Session = Depends(get_session), input_: model.TransactionInput):
    if not crud.account.is_in_database(session, input_.account_id, none_ok=True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    if not crud.payee.is_in_database(session, input_.payee_id, none_ok=True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payee not found")

    if not crud.category.is_in_database(session, input_.category_id, none_ok=True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    row = crud.transaction.create(session, input_)

    return row


@router.get("/{id_}", response_model=model.TransactionOutput)
def read(*, session: Session = Depends(get_session), id_: int = Depends(check_existent_id)):
    row = crud.transaction.get(session, id_)

    return row


@router.get("/", response_model=list[model.TransactionOutput])
def read_many(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    rows = crud.transaction.get_many(session, skip, limit)

    return rows


@router.put("/{id_}", response_model=model.TransactionOutput)
def update(
    *,
    session: Session = Depends(get_session),
    id_: int = Depends(check_existent_id),
    update_: model.TransactionUpdate
):
    row = crud.transaction.update(session, id_, update_)

    return row


@router.delete("/{id_}", response_model=model.TransactionOutput)
def delete(*, session: Session = Depends(get_session), id_: int = Depends(check_existent_id)):
    row = crud.transaction.delete(session, id_)

    return row
