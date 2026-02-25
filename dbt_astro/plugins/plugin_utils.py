from api_client import *
import pandas as pd
from plugin_variables import *
from google.cloud import storage
import io
from datetime import datetime, timedelta


def get_project_id():
    with open(KEY_FILE_PATH, 'r') as f:
        creds_data = json.load(f)
        return creds_data['project_id']


def fetch_account_data():
    accounts_data = get_account()
    accounts_list = accounts_data.get('accounts', [])

    if not accounts_list:
        print("No accounts found for this user.")
        return None

    account_id = accounts_list[0]["id"]

    return {
        'accounts_list': accounts_list,
        'account_id': account_id
    }

def fetch_raw_data(account_id, last_run_timestamp):

    balance_data = get_balance(account_id)
    transactions_data = get_transactions(account_id, last_run_timestamp)
    transactions_list = transactions_data['transactions']

    return {
        'transactions_list': transactions_list,
        'balance_data': balance_data,
    }

def create_dataframe(last_run_timestamp):
    accounts_data = fetch_account_data()
    account_id = accounts_data['account_id']

    raw_data = fetch_raw_data(account_id, last_run_timestamp)

    accounts_list = accounts_data['accounts_list']
    balance_data = raw_data['balance_data']
    transactions_list = raw_data['transactions_list']


    balance_df = pd.DataFrame([balance_data])
    accounts_df = pd.DataFrame(accounts_list)
    transactions_df_clean = clean_transactions(transactions_list)


    return {
        'accounts_df': accounts_df,
        'balance_df': balance_df,
        'transactions_df_clean': transactions_df_clean
    }

# def clean_transactions(transactions_list):
#
#     transactions_df = pd.DataFrame(transactions_list)
#     columns_to_drop = ['fees', 'metadata', 'counterparty', 'attachments', 'labels',
#                        'categories', 'international', 'atm_fees_detailed']
#     transactions_df_stg = transactions_df.drop(columns=columns_to_drop, errors='ignore')
#
#     return transactions_df_stg

def clean_transactions(transactions_list):
    transactions_df = pd.DataFrame(transactions_list)
    columns_to_drop = [
        "fees",
        "metadata",
        "counterparty",
        "attachments",
        "labels",
        "categories",
        "international",
        "atm_fees_detailed",
    ]
    return transactions_df.drop(columns=columns_to_drop, errors="ignore")



def extract_timestamp_since():

    if blob.exists():
        last_run_timestamp = blob.download_as_text().strip()
    else:
        last_run_timestamp = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"Starting run. Fetching data since: {last_run_timestamp}")

    return last_run_timestamp


def upload_timestamp_since():
    current_run_ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    blob.upload_from_string(current_run_ts)
    print(f"Success! Metadata updated. Next run will start from: {current_run_ts}")

def load_df_to_gcs(df, directory_name, file_name):
    bucket = storage_client.bucket("monzo-landing")
    blob = bucket.blob(f"{directory_name}/date={datetime.now().strftime('%Y-%m-%d')}/{file_name}")

    # Use a buffer to avoid writing to local disk
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # The upload_from_string method automatically overwrites if the blob name already exists
    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
    print(f"Uploaded: gs://monzo-landing/{directory_name}/date={datetime.now().strftime('%Y-%m-%d')}/{file_name}")

def load_data(accounts_df, transactions_df_clean, balance_df):
    load_df_to_gcs(accounts_df, "accounts","raw_accounts.csv")
    load_df_to_gcs(transactions_df_clean, "transactions","raw_transactions.csv")
    load_df_to_gcs(balance_df, "balance","raw_balance.csv")



