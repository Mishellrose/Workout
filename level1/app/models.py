from sqlalchemy import Column,String , Integer
from app.database import Base




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False)
    age = Column(Integer, nullable=False)
