terraform {
  required_version = "~> 1.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
  backend "gcs" {
  bucket  = "tf-state-monzo"
  prefix  = "terraform/state"
  }
  }

provider "google" {
  project = var.project_id
  region  = var.region
}
