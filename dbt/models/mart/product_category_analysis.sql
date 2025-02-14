with sales as (
    select * from {{ ref('stg_sales') }}
),

category_metrics as (
    select
        product_category,
        count(distinct transaction_id) as total_transactions,
        sum(quantity) as total_items_sold,
        sum(total_amount) as total_revenue,
        avg(unit_price) as avg_unit_price,
        sum(total_amount) / sum(quantity) as avg_price_per_item
    from sales
    group by product_category
)

select * from category_metrics 