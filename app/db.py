from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_password = os.getenv('dbpass') 
# dbURL = f"postgresql+psycopg://postgres:db_password@localhost:5432/projdata"
dbURL = f"postgresql+psycopg://postgres:Mwy21@localhost:5432/projdata"

engine = create_engine(dbURL)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()