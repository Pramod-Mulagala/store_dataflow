# Configure the Google Cloud provider
provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

# Create a new GCP Project
# resource "google_project" "data_eng_project" {
#   name            = var.project_name
#   project_id      = var.project_id
#   billing_account = var.billing_account_id
# }

# Enable required APIs
resource "google_project_service" "compute_api" {
  project = var.project_id
  service = "compute.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "storage_api" {
  project = var.project_id
  service = "storage.googleapis.com"

  disable_on_destroy = false
}

# Create a GCS bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${var.project_id}-data-lake"
  location      = var.region
  force_destroy = true

  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
}

# Create a Compute Instance
resource "google_compute_instance" "vm_instance" {
  name         = "data-processing-instance"
  machine_type = "e2-medium"
  zone         = "${var.region}-a"

  depends_on = [google_project_service.compute_api]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = "apt-get update && apt-get install -y python3-pip"

  tags = ["data-engineering"]
} 