from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    database_url: str | None = None
    mysql_host: str = "db"
    mysql_port: int = 3306
    mysql_database: str
    mysql_user: str
    mysql_password: str
    secret_key: str = Field(min_length=32)
    encryption_key: str
    encryption_keys: str = ""
    sso_secret_key: str = Field(min_length=32)
    frontend_url: str
    debug: bool = False
    default_admin_login: str
    default_admin_password: str

    @model_validator(mode="after")
    def build_database_url(self):
        if not self.database_url:
            self.database_url = URL.create(
                "mysql+asyncmy",
                username=self.mysql_user,
                password=self.mysql_password,
                host=self.mysql_host,
                port=self.mysql_port,
                database=self.mysql_database,
            ).render_as_string(hide_password=False)
        return self

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore", env_ignore_empty=True)


settings = Settings()
