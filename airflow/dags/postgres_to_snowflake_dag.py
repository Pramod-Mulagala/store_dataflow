from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
import pandas as pd

default_args = {
    'owner': 'Pramod',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['mlgl.pramod@gmail.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def transfer_data_to_snowflake(**context):
    # Get data from PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    df = pg_hook.get_pandas_df("SELECT * FROM raw_sales")
    
    # Load to Snowflake
    snow_hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    
    # Convert DataFrame to CSV string
    csv_buffer = df.to_csv(index=False, header=False)
    
    # Load to Snowflake using internal stage
    snow_hook.run(f"""
        PUT file://{csv_buffer} @%RAW_SALES;
        COPY INTO RAW_SALES 
        FROM @%RAW_SALES
        FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
    """)

with DAG(
    'postgres_to_snowflake_pipeline',
    default_args=default_args,
    description='Load PostgreSQL data to Snowflake',
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_snowflake_table = SnowflakeOperator(
        task_id='create_snowflake_table',
        snowflake_conn_id='snowflake_default',
        sql="""
        CREATE TABLE IF NOT EXISTS RAW_DB.PUBLIC.RAW_SALES (
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

    transfer_data = PythonOperator(
        task_id='transfer_postgres_to_snowflake',
        python_callable=transfer_data_to_snowflake
    )

    create_snowflake_table >> transfer_data 