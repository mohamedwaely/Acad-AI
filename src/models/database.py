from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('db_user', 'postgres')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host', 'localhost')
db_port = os.getenv('db_port', '5432')
db_name = os.getenv('db_name', 'projdata')

dbURL = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


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