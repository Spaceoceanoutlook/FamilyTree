from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    # Admin
    hashed_admin_password: str

    # Photo
    photo_upload_dir: str
    photo_url_prefix: str

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
