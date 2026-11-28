from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from core.database import Base
from auth.policies import get_roles_policies


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    role = Column(String(15), nullable=False, default="analyst")
    password_hash = Column(String(255), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def resources(self) -> list[str]:
        return get_roles_policies(self.role).get("resources", [])

    @property
    def actions(self) -> list[str]:
        return get_roles_policies(self.role).get("actions", [])

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', role='{self.role}', resources={self.resources})>"