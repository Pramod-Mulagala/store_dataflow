variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "data-engineering-1312"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "postgres_password" {
  description = "Password for PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "database_name" {
  description = "Name of the database to create"
  type        = string
  default     = "retail_analytics"
}

variable "database_user" {
  description = "Database user name"
  type        = string
  default     = "postgres"
}

variable "ssh_user" {
  description = "SSH username"
  type        = string
  default     = "ubuntu"
}

variable "ssh_pub_key_path" {
  description = "Path to public SSH key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

# Snowflake Variables
variable "snowflake_account" {
  description = "Snowflake account identifier"
  type        = string
}

variable "snowflake_user" {
  description = "Snowflake username"
  type        = string
}

variable "snowflake_password" {
  description = "Snowflake password"
  type        = string
  sensitive   = true
}

variable "snowflake_warehouse" {
  description = "Snowflake warehouse name"
  type        = string
}

# DBT Variables
variable "dbt_account" {
  description = "Snowflake account for DBT"
  type        = string
}

variable "dbt_user" {
  description = "Snowflake user for DBT operations"
  type        = string
}

variable "dbt_password" {
  description = "Snowflake password for DBT user"
  type        = string
  sensitive   = true
}

variable "dbt_warehouse" {
  description = "Snowflake warehouse for DBT operations"
  type        = string
  default     = "TRANSFORM_WH"
}

variable "dbt_database" {
  description = "DBT target database in Snowflake"
  type        = string
  default     = "RAW_DB"
}

variable "dbt_schema" {
  description = "DBT target schema in Snowflake"
  type        = string
  default     = "PUBLIC"
}

variable "dbt_role" {
  description = "Snowflake role for DBT operations"
  type        = string
  default     = "TRANSFORMER"
}

variable "dbt_threads" {
  description = "Number of threads DBT can use"
  type        = number
  default     = 4
} 