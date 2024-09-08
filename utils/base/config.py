import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv("env/dev.env")

BASE_DIR = Path(__file__).parent.parent.parent

class APISettings(BaseSettings):
    environment: str
    title: str
    domain: str
    docs_user: str
    docs_password: str
    key: str

    class Config:
        env_prefix = "API_"


class DatabaseSettings(BaseSettings):
    postgres_port: int
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    ssl_path: str

    url: str = ""

    class Config:
        env_prefix = "DB_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self):
        ssl_part = ""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}{ssl_part}"
        )
    
class KeySettings(BaseSettings):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algoritm: str = 'RS256'

class S3Settings(BaseSettings):
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str

    class Config:
        env_prefix = 'S3_'


class AppSettings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    key: KeySettings = KeySettings()
    s3: S3Settings = S3Settings()



settings = AppSettings()

if __name__ == '__main__':
    print(settings)
