from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.local_to_snowflake import LocalFileToSnowflakeOperator

default_args = {
    'owner': 'Pramod',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['mlgl.pramod@gmail.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

SNOWFLAKE_CONN_ID = "snowflake_default"
SNOWFLAKE_DATABASE = "RAW_DB"
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_STAGE = "CSV_STAGE"
SNOWFLAKE_TABLE = "RAW_SALES"

with DAG(
    'csv_to_snowflake_pipeline',
    default_args=default_args,
    description='Load CSV data to Snowflake',
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_table = SnowflakeOperator(
        task_id='create_raw_table',
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE} (
            transaction_id VARCHAR,
            date DATE,
            store_id VARCHAR,
            product_category VARCHAR,
            product_name VARCHAR,
            quantity INTEGER,
            unit_price FLOAT,
            total_amount FLOAT,
            payment_method VARCHAR,
            customer_id VARCHAR,
            customer_age INTEGER,
            customer_gender VARCHAR,
            customer_location VARCHAR
        )
        """
    )

    load_to_snowflake = LocalFileToSnowflakeOperator(
        task_id='load_csv_to_snowflake',
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        table=SNOWFLAKE_TABLE,
        schema=SNOWFLAKE_SCHEMA,
        database=SNOWFLAKE_DATABASE,
        stage=SNOWFLAKE_STAGE,
        file_path='retail_store_sales_cleaned.csv',
        file_format="(type = 'CSV', skip_header = 1)"
    )

    create_table >> load_to_snowflake 