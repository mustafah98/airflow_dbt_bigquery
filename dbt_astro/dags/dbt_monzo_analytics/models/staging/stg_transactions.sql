{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

select
    amount / 100.0 AS amount,
    created,
    updated,
    settled,
    created AS transaction_timestamp,
    DATE(created) AS transaction_date,
    TIME(created) AS transaction_time,
    id,
    category,
    description,
    COALESCE(merchant,'-1') as merchant_id,
    notes,
    decline_reason,
    currency

from {{ source('monzo_bronze', 'bronze_transactions') }}


{% if is_incremental() %}
    where created >= (select max(created) from {{ this }} )
{% endif %}

