from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    tokens = Column(Integer, nullable=False, server_default=text('3'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))