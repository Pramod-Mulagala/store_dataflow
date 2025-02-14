terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Enable required APIs
resource "google_project_service" "sql_admin" {
  service = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  disable_on_destroy = false
}

# VPC Network
resource "google_compute_network" "vpc_network" {
  name                    = "retail-analytics-vpc"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "retail-analytics-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc_network.id
  region        = var.region
}

# Firewall rules
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["5432", "8080", "5555"]
  }

  source_ranges = ["10.0.0.0/24"]
}

# Allow external access to Airflow UI
resource "google_compute_firewall" "allow_airflow_ui" {
  name    = "allow-airflow-ui"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["8080", "22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["airflow"]
}

# Airflow Instance
resource "google_compute_instance" "airflow_instance" {
  name         = "airflow-server"
  machine_type = "e2-medium"
  zone         = var.zone

  metadata = {
    ssh-keys = "${var.ssh_user}:${file(var.ssh_pub_key_path)}"
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 30
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.subnet.name
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = file("${path.module}/scripts/airflow_setup.sh")

  service_account {
    email  = google_service_account.airflow_service_account.email
    scopes = ["cloud-platform"]
  }

  tags = ["airflow"]
}

# PostgreSQL Instance
resource "google_sql_database_instance" "postgres" {
  name             = "retail-postgres-instance"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "airflow-server"
        value = google_compute_instance.airflow_instance.network_interface[0].access_config[0].nat_ip
      }
    }
    backup_configuration {
      enabled = false
    }
    database_flags {
      name  = "max_connections"
      value = "25"
    }
  }
  deletion_protection = false
}

# Create a database
resource "google_sql_database" "database" {
  name     = "retail_analytics"
  instance = google_sql_database_instance.postgres.name
}

# Create a user
resource "google_sql_user" "users" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres.name
  password = var.postgres_password
}

# Service Account for Airflow
resource "google_service_account" "airflow_service_account" {
  account_id   = "airflow-service-account"
  display_name = "Airflow Service Account"
}

# IAM roles for the service account
resource "google_project_iam_member" "airflow_roles" {
  for_each = toset([
    "roles/storage.objectViewer",
    "roles/bigquery.dataViewer",
    "roles/cloudsql.client"
  ])
  
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.airflow_service_account.email}"
} 