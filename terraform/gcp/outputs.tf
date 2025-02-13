output "project_id" {
  value = var.project_id
}

output "bucket_name" {
  value = google_storage_bucket.data_lake_bucket.name
}

output "compute_instance_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
} 