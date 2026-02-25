import {
  id = "projects/${var.project_id}/serviceAccounts/${var.service_account_id}@${var.project_id}.iam.gserviceaccount.com"
  to = google_service_account.pipeline_sa
}

# Create the Service Account
resource "google_service_account" "pipeline_sa" {
  account_id   = var.service_account_id
  display_name = "Monzo Pipeline Service Account"
}

# Grant Bucket Access (Read/Write for the API ingest)
resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.landing_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Grant BigQuery Access (To run DBT and load data)
resource "google_project_iam_member" "bq_owner" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}
