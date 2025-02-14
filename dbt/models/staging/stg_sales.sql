with source as (
    select * from {{ source('raw_db', 'raw_sales') }}
),

staged as (
    select
        transaction_id,
        date as transaction_date,
        store_id,
        product_category,
        product_name,
        quantity,
        unit_price,
        total_amount,
        payment_method,
        customer_id,
        customer_age,
        customer_gender,
        customer_location,
        current_timestamp() as loaded_at
    from source
)

select * from staged 