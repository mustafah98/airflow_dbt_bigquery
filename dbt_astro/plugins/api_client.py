import requests
from plugin_variables import MONZO_API_BASE, HEADERS
# from google.cloud import bigquery
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

# pip install --upgrade google-cloud-bigquery
def get_method(suffix, params=None):
    url = MONZO_API_BASE + suffix
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def get_account():
    url = MONZO_API_BASE + "/accounts"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_balance(account_id):
    url = MONZO_API_BASE + "/balance"

    PARAMS = {
        "account_id": account_id,
        "limit": 100
    }

    response = requests.get(url, headers=HEADERS, params=PARAMS)
    return response.json()


def get_transactions(account_id, last_run_timestamp):
    url = MONZO_API_BASE + "/transactions"

    PARAMS = {
        "account_id": account_id,
        "since": last_run_timestamp,
        "limit": 100
    }

    response = requests.get(url, headers=HEADERS, params=PARAMS,  timeout=30)

    return response.json()

#
# def load_to_bigquery(df, table_name, project_id, dataset_id, client):
#     table_id = f"{project_id}.{dataset_id}.{table_name}"
#
#     job_config = bigquery.LoadJobConfig(
#         write_disposition="WRITE_APPEND",
#     )
#
#     job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
#     job.result()
#
#     print(f"Loaded {len(df)} rows to {table_id}")
