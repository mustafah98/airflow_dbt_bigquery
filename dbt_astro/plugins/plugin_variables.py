import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import bigquery, storage
from env_variables import ACCESS_TOKEN
from datetime import datetime, timedelta

load_dotenv(find_dotenv())

BUCKET_NAME = "monzo-landing"

plugin_dir = Path(__file__).parent.absolute()
BASE_DIR = plugin_dir.parent

KEY_FILE_PATH = (
    BASE_DIR / "dags/dbt_monzo_analytics/creds/project-424d7fe3-5b4f-48a0-a49-b28d32165ebb.json"
)

credentials = service_account.Credentials.from_service_account_file(str(KEY_FILE_PATH))

client = bigquery.Client(project=credentials.project_id, credentials=credentials)
storage_client = storage.Client(project=credentials.project_id, credentials=credentials)

GCS_BASE_PREFIX = os.getenv("GCS_BASE_PREFIX", "monzo/raw")

MONZO_API_BASE = "https://api.monzo.com"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

bucket = storage_client.bucket("monzo-landing")
blob = bucket.blob("metadata/last_updated.txt")

if blob.exists():
    last_run_timestamp = blob.download_as_text().strip()
else:
    last_run_timestamp = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
