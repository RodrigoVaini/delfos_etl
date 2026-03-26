import os
import sys

import httpx
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from transform import (
    transform_10min,
    normalize,
    upsert_signals,
    apply_signal_ids,
)

load_dotenv(".env.local")

TARGET_DB = (
    f"postgresql://{os.getenv('TARGET_DB_USER')}:"
    f"{os.getenv('TARGET_DB_PASSWORD')}@"
    f"{os.getenv('TARGET_DB_HOST')}:"
    f"{os.getenv('TARGET_DB_PORT')}/"
    f"{os.getenv('TARGET_DB_NAME')}"
)

API_URL = os.getenv("API_BASE_URL")


def run_etl(date_str: str):
    start = f"{date_str}T00:00:00"
    end = f"{date_str}T23:59:59"

    response = httpx.get(
        f"{API_URL}/data",
        params={
            "start": start,
            "end": end,
            "variables": ["wind_speed", "power"],
        },
        timeout=30.0,
    )
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    if df.empty:
        print("Sem dados para o dia.")
        return

    df_agg = transform_10min(df)
    df_agg = df_agg.fillna(0)

    df_norm = normalize(df_agg)

    engine = create_engine(TARGET_DB)

    mapping = upsert_signals(df_norm, engine)
    df_final = apply_signal_ids(df_norm, mapping)

    start_ts = pd.Timestamp(f"{date_str} 00:00:00")
    end_ts = pd.Timestamp(f"{date_str} 23:59:59")

    with engine.begin() as conn:
        conn.execute(
            text("""
                DELETE FROM data
                WHERE timestamp BETWEEN :start_ts AND :end_ts
            """),
            {"start_ts": start_ts, "end_ts": end_ts},
        )

    df_final.to_sql("data", engine, if_exists="append", index=False)

    print("ETL finalizado com sucesso.")
    print(f"Data processada: {date_str}")
    print(f"Linhas inseridas: {len(df_final)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Informe a data no formato YYYY-MM-DD")
    run_etl(sys.argv[1])