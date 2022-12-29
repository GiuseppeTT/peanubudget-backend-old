from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.crud import Crud
from app.database import get_session


class ExistentIdChecker:
    def __init__(self, model_name, crud: Crud):
        self.model_name = model_name
        self.crud = crud

    def __call__(self, id_: int, session: Session = Depends(get_session)) -> int:
        if not self.crud.is_in_database(session, id_):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model_name} not found"
            )

        return id_
