# Docker with PostgreSQL Setup

This directory contains Docker configurations for setting up a PostgreSQL database and pgAdmin interface.

## Prerequisites

- Docker
- Docker Compose
- Python 3.11+
- Poetry (for Python dependency management)

## Quick Start

1. Build and start the containers:
   ```bash
   cd docker
   docker-compose up -d
   ```

2. Access pgAdmin:
   - URL: http://localhost:8080
   - Email: admin@admin.com
   - Password: admin123

3. Connect to PostgreSQL:
   - Host: postgres
   - Port: 5432
   - Database: zoomcamp
   - Username: admin
   - Password: admin123

4. Run the sample Python script:
   ```bash
   poetry run python scripts/ingest_data.py
   ```

## Directory Structure 