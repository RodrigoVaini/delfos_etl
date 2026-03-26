import pandas as pd
from sqlalchemy import text


def transform_10min(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    agg = df.resample("10min").agg({
        "wind_speed": ["mean", "min", "max", "std"],
        "power": ["mean", "min", "max", "std"],
    })

    agg.columns = [f"{col[0]}_{col[1]}" for col in agg.columns]
    agg = agg.reset_index()

    return agg


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    records = []

    for _, row in df.iterrows():
        timestamp = row["timestamp"]

        for col in df.columns:
            if col == "timestamp":
                continue

            records.append({
                "timestamp": timestamp,
                "signal_name": col,
                "value": row[col],
            })

    return pd.DataFrame(records)


def upsert_signals(df: pd.DataFrame, engine):
    signal_names = df["signal_name"].unique().tolist()

    with engine.begin() as conn:
        for name in signal_names:
            conn.execute(
                text("""
                    INSERT INTO signal (name)
                    VALUES (:name)
                    ON CONFLICT (name) DO NOTHING
                """),
                {"name": name},
            )

        result = conn.execute(
            text("""
                SELECT id, name
                FROM signal
                WHERE name = ANY(:names)
            """),
            {"names": signal_names},
        )

        mapping = {row.name: row.id for row in result}

    return mapping


def apply_signal_ids(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    df["signal_id"] = df["signal_name"].map(mapping)
    return df[["timestamp", "signal_id", "value"]]