import os
from airflow.models import Variable

# ACCESS_TOKEN = Variable.get("MONZO_ACCESS_TOKEN", default_var=None)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GMAIL_ACCOUNT = os.getenv("GMAIL_ACCOUNT")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
DATASET_ID = os.getenv("DATASET_ID")


