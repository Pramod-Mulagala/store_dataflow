output "airflow_ip" {
  description = "Public IP address of the Airflow instance"
  value       = google_compute_instance.airflow_instance.network_interface[0].access_config[0].nat_ip
}

output "postgres_connection" {
  description = "PostgreSQL connection name"
  value       = google_sql_database_instance.postgres.connection_name
}

output "postgres_public_ip" {
  description = "PostgreSQL public IP address"
  value       = google_sql_database_instance.postgres.public_ip_address
}

output "postgres_instance_name" {
  description = "PostgreSQL instance name"
  value       = google_sql_database_instance.postgres.name
} 