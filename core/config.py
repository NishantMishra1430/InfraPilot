import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

class Credentials:
    # DataBase Credentials 
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "auth_db")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "nishant")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    
    # LocalStack Credentials 
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    LOCALSTACK_AUTH_TOKEN = os.getenv("LOCALSTACK_AUTH_TOKEN", "test")
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://157.173.121.36:4566")
    
    # Default Boot User 
    DEFAULT_USERNAME: str = os.getenv("DEFAULT_USERNAME", "admin")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "admin")

    # DB URL 
    @property
    def auth_db_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
cred = Credentials()