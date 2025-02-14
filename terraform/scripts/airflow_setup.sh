#!/bin/bash

# Update and install dependencies
apt-get update
apt-get install -y python3-pip postgresql-client

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# # Clone your project repository
# git clone <your-repo-url> /opt/retail-analytics

# # Set up environment variables
# cat <<EOF > /opt/retail-analytics/.env
# POSTGRES_HOST=${google_sql_database_instance.postgres.ip_address}
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=${var.postgres_password}
# SNOWFLAKE_ACCOUNT=<your-snowflake-account>
# SNOWFLAKE_USER=<your-snowflake-user>
# SNOWFLAKE_PASSWORD=<your-snowflake-password>
# SNOWFLAKE_WAREHOUSE=<your-snowflake-warehouse>
# EOF

# Start Airflow using Docker Compose
# cd /opt/retail-analytics
# docker-compose up -d 