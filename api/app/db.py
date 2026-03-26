import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = (
    f"postgresql://{os.getenv('SOURCE_DB_USER')}:"
    f"{os.getenv('SOURCE_DB_PASSWORD')}@"
    f"{os.getenv('SOURCE_DB_HOST')}:"
    f"{os.getenv('SOURCE_DB_PORT')}/"
    f"{os.getenv('SOURCE_DB_NAME')}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)