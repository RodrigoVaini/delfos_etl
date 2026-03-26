import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(".env.local")

DB_HOST = os.getenv("SOURCE_DB_HOST")
DB_PORT = os.getenv("SOURCE_DB_PORT")
DB_NAME = os.getenv("SOURCE_DB_NAME")
DB_USER = os.getenv("SOURCE_DB_USER")
DB_PASSWORD = os.getenv("SOURCE_DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

start = pd.Timestamp("2025-01-01 00:00:00")
end = start + pd.Timedelta(days=10) - pd.Timedelta(minutes=1)

df = pd.DataFrame({
    "timestamp": pd.date_range(start=start, end=end, freq="1min"),
})

df["wind_speed"] = np.random.uniform(0, 20, len(df)).round(2)
df["power"] = np.random.uniform(0, 1000, len(df)).round(2)
df["ambient_temperature"] = np.random.uniform(15, 35, len(df)).round(2)

df.to_sql("data", engine, if_exists="replace", index=False)

print("Dados gerados com sucesso.")
print(f"Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
print(f"Total de registros: {len(df)}")