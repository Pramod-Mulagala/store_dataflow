from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator

default_args = {
    'owner': 'Pramod',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Update these values
PROJECT_ID = "data-engineering-1312"
BUCKET_NAME = f"{PROJECT_ID}-data-lake"
DATASET_NAME = "de_dataset"

with DAG(
    'gcs_to_bigquery_pipeline',
    default_args=default_args,
    description='Load data from GCS to BigQuery',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Create GCS bucket if it doesn't exist
    create_bucket = GCSCreateBucketOperator(
        task_id='create_bucket',
        bucket_name=BUCKET_NAME,
        project_id=PROJECT_ID,
        location='US-CENTRAL1'
    )

    # Load data from GCS to BigQuery
    load_to_bigquery = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=['data/*.csv'],  # Adjust based on your file pattern
        destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_NAME}.sample_table',
        schema_fields=[
            {'name': 'id', 'type': 'INTEGER'},
            {'name': 'name', 'type': 'STRING'},
            {'name': 'value', 'type': 'FLOAT'}
        ],
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        skip_leading_rows=1
    )

    create_bucket >> load_to_bigquery 