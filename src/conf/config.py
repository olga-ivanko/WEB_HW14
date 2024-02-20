from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    email_username: str
    email_password: str
    email_from: str
    email_port: int
    email_server: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_domain: str
    postgres_port: int
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
