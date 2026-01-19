FROM astrocrpublic.azurecr.io/runtime:3.1-9

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate

COPY dags/dbt_monzo_analytics/creds/*.json /app/creds/keyfile.json