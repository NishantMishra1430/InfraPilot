from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

from core.config import cred
from core.exceptions import InfrastructureOfflineError

engine = create_engine(cred.auth_db_url, pool_pre_ping=True, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """
    Creates a new database session. 
    Catches raw PostgreSQL offline errors and raises clean InfrastructureOfflineError.
    """
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        yield session
    except OperationalError as raw_err:
        raise InfrastructureOfflineError(
            f"Auth Database at {cred.POSTGRES_PORT} is unreachable. "
            "Fix: Run 'docker compose up -d auth-db' first."
        ) from raw_err
    finally:
        session.close()