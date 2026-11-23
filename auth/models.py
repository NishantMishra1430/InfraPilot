# importing Libraries and Functions 
# Define a class of user 
# in which 
# name, role, hash_password, resources, joined_at
# import that class into a Variable
from sqlalchemy import Column, Integer, JSON, DateTime, String 
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True) # datatype, define_is_<id>_is_a_Unique_coloum_or_not, indexing
    username = Column(String(50), unique=True, index=True, nullable=False, )# unique defines a unique username, nullable: this field cannot be empty
    role = Column(String(15), nullable=False, default="Viewer")
    password_hash = Column(String(255), nullable=False)
    resources = Column(JSON, nullable=False, default=list)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(username: '{self.username}', role: '{self.role}', resources: {self.resources})>"