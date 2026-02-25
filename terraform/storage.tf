resource "google_storage_bucket" "landing_bucket" {
  name          = "monzo-landing"
  location      = var.region
  force_destroy = false
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket" "tf_state_bucket" {
  name     = "tf-state-monzo" # Must be globally unique
  location = "EU"
  force_destroy = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
