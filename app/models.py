from sqlalchemy import Column, Integer, String, Boolean, Text, Float
from pgvector.sqlalchemy import Vector
from app.db import Base
metadata=Base.metadata
print('MetaDAta:', metadata,'\n')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    degree = Column(String(1), nullable=False)
    added_by = Column(String(100), nullable=False)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    uploader = Column(String(100), nullable=False)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(Text, nullable=False)
    supervisor = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    embedding = Column(Vector(768), nullable=False) 

class PreProjects(Base):
    __tablename__ = "preprojects"

    id= Column(Integer, primary_key=True)
    title= Column(String(100), unique=True, nullable=False)
    description= Column(Text, nullable=False)
    year= Column(Integer, nullable=False)
    maxSimScore= Column(Float, nullable=True)


