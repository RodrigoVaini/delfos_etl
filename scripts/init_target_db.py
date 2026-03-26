import os

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)

load_dotenv(".env.local")

DB_HOST = os.getenv("TARGET_DB_HOST")
DB_PORT = os.getenv("TARGET_DB_PORT")
DB_NAME = os.getenv("TARGET_DB_NAME")
DB_USER = os.getenv("TARGET_DB_USER")
DB_PASSWORD = os.getenv("TARGET_DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

metadata = MetaData()

signal = Table(
    "signal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True),
)

data = Table(
    "data",
    metadata,
    Column("timestamp", DateTime, nullable=False),
    Column("signal_id", Integer, ForeignKey("signal.id"), nullable=False),
    Column("value", Float),
    UniqueConstraint("timestamp", "signal_id", name="uq_data_timestamp_signal"),
)

metadata.create_all(engine)

print("Banco alvo inicializado com sucesso.")