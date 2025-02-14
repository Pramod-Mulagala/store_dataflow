from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
import pandas as pd
import logging

default_args = {
    'owner': 'Pramod',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['mlgl.pramod@gmail.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def check_data_quality(**context):
    snow_hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    
    checks = [
        {
            'name': 'null_check',
            'query': """
                SELECT column_name, COUNT(*) as null_count
                FROM RAW_DB.PUBLIC.RAW_SALES
                WHERE transaction_id IS NULL 
                   OR date IS NULL 
                   OR total_amount IS NULL
                GROUP BY column_name
            """
        },
        {
            'name': 'duplicate_check',
            'query': """
                SELECT transaction_id, COUNT(*) as duplicate_count
                FROM RAW_DB.PUBLIC.RAW_SALES
                GROUP BY transaction_id
                HAVING COUNT(*) > 1
            """
        },
        {
            'name': 'negative_values_check',
            'query': """
                SELECT 'quantity' as column_name, COUNT(*) as negative_count
                FROM RAW_DB.PUBLIC.RAW_SALES
                WHERE quantity < 0
                UNION ALL
                SELECT 'total_amount' as column_name, COUNT(*) as negative_count
                FROM RAW_DB.PUBLIC.RAW_SALES
                WHERE total_amount < 0
            """
        },
        {
            'name': 'date_range_check',
            'query': """
                SELECT 
                    MIN(date) as earliest_date,
                    MAX(date) as latest_date,
                    COUNT(*) as total_records
                FROM RAW_DB.PUBLIC.RAW_SALES
            """
        }
    ]
    
    results = {}
    for check in checks:
        df = snow_hook.get_pandas_df(check['query'])
        results[check['name']] = df.to_dict()
        
        if not df.empty:
            logging.warning(f"Quality check '{check['name']}' failed:\n{df}")
    
    return results

with DAG(
    'snowflake_data_quality_checks',
    default_args=default_args,
    description='Snowflake data quality checking pipeline',
    schedule_interval='@daily',
    catchup=False
) as dag:

    quality_check_task = PythonOperator(
        task_id='check_data_quality',
        python_callable=check_data_quality,
        provide_context=True
    ) 