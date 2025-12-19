variable "project_id" { type = string }
variable "region" {
  type    = string
  default = "europe-west9"
}
variable "service_name" { type = string }
variable "image" { type = string }
variable "credentials_path" {
  type        = string
  description = "Path to the GCP service account key JSON"

}
