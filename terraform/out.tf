# to easily retrieve the Cloud Run service URL
output "service_url" {
  value = google_cloud_run_v2_service.service.uri
}
