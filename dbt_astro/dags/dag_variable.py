import os

CONNECTION_NAME = 'db_conn'
DATASET = os.getenv("DATASET_ID")

PROFILES_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt_monzo_analytics/profiles.yml"
EXECUTION_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt_monzo_analytics"


