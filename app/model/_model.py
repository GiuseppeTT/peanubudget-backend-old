from sqlmodel import Field, SQLModel


class ModelInput(SQLModel):
    pass


# `id` can be None when not committed, but don't tell mypy 🤫
class ModelDatabase(SQLModel):
    id: int = Field(default=None, primary_key=True)


class ModelOutput(SQLModel):
    id: int

    class Config:
        orm_mode = True


class ModelUpdate(SQLModel):
    pass
