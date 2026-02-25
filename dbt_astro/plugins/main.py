from google.cloud import bigquery
from plugin_utils import create_dataframe, load_data
from datetime import datetime
from plugin_variables import storage_client, bucket, blob, last_run_timestamp

def app_runner():

    print(f"Starting run. Fetching data since: {last_run_timestamp}")

    dataframes = create_dataframe(last_run_timestamp)
    
    accounts_df = dataframes['accounts_df']
    transactions_df_clean = dataframes['transactions_df_clean']
    balance_df = dataframes['balance_df']
    
    print("loading data to gcs...")
    load_data(accounts_df, transactions_df_clean, balance_df)

    current_run_ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    blob.upload_from_string(current_run_ts)


if __name__ == "__main__":
    app_runner()
