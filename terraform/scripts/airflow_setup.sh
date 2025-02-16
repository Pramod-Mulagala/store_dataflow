#!/bin/bash

# Update and install dependencies
apt-get update
apt-get install -y python3-pip postgresql-client git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone the repository
git clone https://github.com/Pramod-Mulagala/retail-analytics-data.git /opt/retail-analytics
cd /opt/retail-analytics

# Create Airflow directory structure
mkdir -p airflow/{dags,logs,plugins,config,gcp}
mkdir -p airflow/dbt/profiles
chmod -R 777 airflow/

# Create DBT profiles.yml
cat <<EOF > airflow/dbt/profiles/profiles.yml
retail_analytics:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: "{{ env_var('DBT_SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_SNOWFLAKE_USER') }}"
      password: "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('DBT_SNOWFLAKE_ROLE') }}"
      warehouse: "{{ env_var('DBT_SNOWFLAKE_WAREHOUSE') }}"
      database: "{{ env_var('DBT_SNOWFLAKE_DATABASE') }}"
      schema: "{{ env_var('DBT_SNOWFLAKE_SCHEMA') }}"
      threads: "{{ env_var('DBT_THREADS', '4') }}"
      client_session_keep_alive: False
      query_tag: dbt
EOF

# Set up environment variables
cat <<EOF > airflow/.env
# PostgreSQL Configuration
POSTGRES_HOST=${google_sql_database_instance.postgres.ip_address}
POSTGRES_USER=postgres
POSTGRES_PASSWORD=${var.postgres_password}
POSTGRES_DB=airflow

# Snowflake Configuration
SNOWFLAKE_ACCOUNT=${var.snowflake_account}
SNOWFLAKE_USER=${var.snowflake_user}
SNOWFLAKE_PASSWORD=${var.snowflake_password}
SNOWFLAKE_WAREHOUSE=${var.snowflake_warehouse}

# DBT Configuration
DBT_SNOWFLAKE_ACCOUNT=${var.dbt_account}
DBT_SNOWFLAKE_USER=${var.dbt_user}
DBT_SNOWFLAKE_PASSWORD=${var.dbt_password}
DBT_SNOWFLAKE_ROLE=${var.dbt_role}
DBT_SNOWFLAKE_WAREHOUSE=${var.dbt_warehouse}
DBT_SNOWFLAKE_DATABASE=${var.dbt_database}
DBT_SNOWFLAKE_SCHEMA=${var.dbt_schema}
DBT_THREADS=${var.dbt_threads}

# GCP Configuration
PROJECT_ID=data-engineering-1312
REGION=us-central1
DATA_LAKE_BUCKET=data-engineering-1312-data-lake
DATASET_ID=de_dataset
EOF

# Start Airflow
cd airflow
docker-compose up -d 