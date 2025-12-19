terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_path)
}

resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = var.image

      ports {
        container_port = 8501
      }
    }
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}

# I prefer to manually set the IAM permissions via GCP console for more control
# resource "google_cloud_run_service_iam_member" "invoker" {
#   service  = google_cloud_run_v2_service.service.name
#   location = var.region
#   role     = "roles/run.invoker"
#   member   = var.invoker_member
# }
