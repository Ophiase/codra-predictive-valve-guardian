variable "project_id" { type = string }
variable "region" {
  type    = string
  default = "europe-west9"
}
variable "service_name" {
  type = string
  default = "predictive-valve-guardian-service"
  }
variable "image" { type = string }
variable "credentials_path" {
  type        = string
  description = "Path to the GCP service account key JSON"

}

variable "invoker_member" {
  type        = string
  description = "IAM member allowed to invoke the Cloud Run service. Example: allUsers, user:email@gmail.com, serviceAccount:sa@project.iam.gserviceaccount.com"
  default     = "allUsers"
}
