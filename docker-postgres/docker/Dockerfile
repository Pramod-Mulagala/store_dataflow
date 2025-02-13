FROM postgres:15

# Environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123
ENV POSTGRES_DB=retail_store_sales

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432 