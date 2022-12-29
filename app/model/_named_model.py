from typing import Optional

from sqlmodel import Field

from app.model._model import ModelDatabase, ModelInput, ModelOutput, ModelUpdate


class NamedModelInput(ModelInput):
    name: str


class NamedModelDatabase(ModelDatabase):
    name: str = Field(unique=True, index=True)


class NamedModelOutput(ModelOutput):
    name: str


class NamedModelUpdate(ModelUpdate):
    name: Optional[str] = None
