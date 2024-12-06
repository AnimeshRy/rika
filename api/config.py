import re
from typing import Any
from typing_extensions import Self

from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def remove_postgresql_variants(dsn: str) -> str:
    """Remove the 'driver' part from a connections string, if one is present in the URL schema

    ORM libraries like sqlalchemy require the driver part for non-default drivers.
    For example, sqlalchemy default to psycopg2 for PostgreSQL, so one need to specify
    'postgresql+psycopy' as the scheme for using psycopg3.

    Args:
        dsn (str): The connection string

    Returns:
        str: The connection string without the driver

    """

    pattern = r"postgresql\+psycopg(?:2(?:cffi)?)?"
    return re.sub(pattern, "postgresql", dsn)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    llm: dict[str, Any] = Field(default_factory=lambda: {"api_key": "NOT_SET"})
    postgresql_primary_url: PostgresDsn = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/rika"
    ) # Primary Database URL, Read/Write
    postgresql_standy_url: PostgresDsn | None = None # Standby Database URL, Read Only. Defaults to Primary

    @model_validator(mode="after")
    def set_default_standby_url(self: Self) -> Self:
        if self.postgresql_standy_url is None:
            self.postgresql_standy_url = self.postgresql_primary_url
        return self

    @property
    def psycopg_primary_url(self) -> str:
        return remove_postgresql_variants(str(self.postgresql_primary_url))

    @property
    def psycopg_standby_url(self) -> str | None:
        return remove_postgresql_variants(str(self.postgresql_standy_url))

settings = Settings()
