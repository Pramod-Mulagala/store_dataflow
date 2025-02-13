from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
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

PROJECT_ID = "data-engineering-1312"
DATASET_NAME = "de_dataset"

def check_data_quality(**context):
    bq_hook = BigQueryHook(use_legacy_sql=False)
    
    # Example quality checks
    checks = [
        {
            'name': 'null_check',
            'query': f"""
                SELECT column_name, COUNT(*) as null_count
                FROM `{PROJECT_ID}.{DATASET_NAME}.sample_table`
                WHERE column_name IS NULL
                GROUP BY column_name
            """
        },
        {
            'name': 'duplicate_check',
            'query': f"""
                SELECT id, COUNT(*) as duplicate_count
                FROM `{PROJECT_ID}.{DATASET_NAME}.sample_table`
                GROUP BY id
                HAVING COUNT(*) > 1
            """
        }
    ]
    
    results = {}
    for check in checks:
        df = bq_hook.get_pandas_df(check['query'])
        results[check['name']] = df.to_dict()
        
        if not df.empty:
            logging.warning(f"Quality check '{check['name']}' failed:\n{df}")
    
    return results

with DAG(
    'data_quality_checks',
    default_args=default_args,
    description='Data quality checking pipeline',
    schedule_interval='@daily',
    catchup=False
) as dag:

    quality_check_task = PythonOperator(
        task_id='check_data_quality',
        python_callable=check_data_quality,
        provide_context=True
    ) 