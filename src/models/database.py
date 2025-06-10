from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

# URL-encode the password to handle special characters
db_password = urllib.parse.quote_plus(os.getenv('db_password'))

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('db_user')}:{db_password}@"
    f"{os.getenv('db_host')}:{os.getenv('db_port')}/"
    f"{os.getenv('db_name')}?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()