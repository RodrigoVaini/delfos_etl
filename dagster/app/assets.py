import httpx
import pandas as pd
from dagster import asset, DailyPartitionsDefinition

from transform import (
    transform_10min,
    normalize,
    upsert_signals,
    apply_signal_ids,
)

daily_partitions = DailyPartitionsDefinition(start_date="2025-01-01")


@asset(
    partitions_def=daily_partitions,
    required_resource_keys={"source_api", "target_db"},
)
def etl_asset(context):
    date = context.partition_key

    start = f"{date}T00:00:00"
    end = f"{date}T23:59:59"

    url = f"{context.resources.source_api['base_url']}/data"

    response = httpx.get(
        url,
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
        context.log.info("Sem dados para o dia.")
        return

    df_agg = transform_10min(df).fillna(0)
    df_norm = normalize(df_agg)

    engine = context.resources.target_db

    mapping = upsert_signals(df_norm, engine)
    df_final = apply_signal_ids(df_norm, mapping)

    start_ts = pd.Timestamp(f"{date} 00:00:00")
    end_ts = pd.Timestamp(f"{date} 23:59:59")

    from sqlalchemy import text
    with engine.begin() as conn:
        conn.execute(
            text("""
                DELETE FROM data
                WHERE timestamp BETWEEN :start_ts AND :end_ts
            """),
            {"start_ts": start_ts, "end_ts": end_ts},
        )

    df_final.to_sql("data", engine, if_exists="append", index=False)

    context.log.info(f"ETL finalizado com sucesso para {date}")