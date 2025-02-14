from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import io
from google.cloud import storage

default_args = {
    'owner': 'Pramod',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['mlgl.pramod@gmail.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_csv_to_postgres(**context):
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    
    # First upload CSV to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket('retail-analytics-data')
    blob = bucket.blob('retail_store_sales_cleaned.csv')
    blob.upload_from_filename('retail_store_sales_cleaned.csv')
    
    # Read CSV file from GCS
    df = pd.read_csv(f'gs://retail-analytics-data/retail_store_sales_cleaned.csv')
    
    # Create a connection to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    
    # Save dataframe to PostgreSQL
    with conn.cursor() as cur:
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        
        cur.copy_from(output, 'raw_sales', null='', columns=df.columns)
        conn.commit()

with DAG(
    'csv_to_postgres_pipeline',
    default_args=default_args,
    description='Load CSV data to PostgreSQL',
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_table = PostgresOperator(
        task_id='create_raw_table',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS raw_sales (
            transaction_id VARCHAR(50),
            date DATE,
            store_id VARCHAR(20),
            product_category VARCHAR(100),
            product_name VARCHAR(200),
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            payment_method VARCHAR(50),
            customer_id VARCHAR(50),
            customer_age INTEGER,
            customer_gender VARCHAR(10),
            customer_location VARCHAR(100)
        );
        """
    )

    load_data = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres
    )

    create_table >> load_data 