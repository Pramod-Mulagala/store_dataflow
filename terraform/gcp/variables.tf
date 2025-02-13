variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
}

variable "project_name" {
  description = "Your GCP Project Name"
  type        = string
}

variable "billing_account_id" {
  description = "Your GCP Billing Account ID"
  type        = string
}

variable "credentials_file" {
  description = "Path to your GCP service account key file"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}