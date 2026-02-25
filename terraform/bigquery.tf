# Bronze / Raw Layer
resource "google_bigquery_dataset" "bronze" {
  dataset_id = "monzo_bronze"
  location   = var.region
}

# Silver / Staging Layer
resource "google_bigquery_dataset" "silver" {
  dataset_id = "monzo_silver"
  location   = var.region
}

# Gold / Analytics Layer
resource "google_bigquery_dataset" "gold" {
  dataset_id = "monzo_gold"
  location   = var.region
}
