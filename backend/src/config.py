from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    encryption_key: str
    sso_secret_key: str = ""
    frontend_url: str
    default_admin_login: str
    default_admin_password: str

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")


settings = Settings()
