import os
from dagster import resource
from sqlalchemy import create_engine


@resource
def source_api():
    return {
        "base_url": os.getenv("API_BASE_URL")
    }


@resource
def target_db():
    engine = create_engine(
        f"postgresql://{os.getenv('TARGET_DB_USER')}:"
        f"{os.getenv('TARGET_DB_PASSWORD')}@"
        f"{os.getenv('TARGET_DB_HOST')}:"
        f"{os.getenv('TARGET_DB_PORT')}/"
        f"{os.getenv('TARGET_DB_NAME')}"
    )
    return engine