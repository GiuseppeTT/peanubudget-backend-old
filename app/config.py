from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_FQDN: str

    class Config:
        env_file = ".env"


settings = Settings()
