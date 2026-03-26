from dagster import Definitions, ScheduleDefinition, define_asset_job

from assets import etl_asset
from resources import source_api, target_db

resources = {
    "source_api": source_api,
    "target_db": target_db,
}

etl_job = define_asset_job(name="etl_job", selection=["etl_asset"])

daily_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="0 2 * * *",
)

defs = Definitions(
    assets=[etl_asset],
    jobs=[etl_job],
    resources=resources,
    schedules=[daily_schedule],
)