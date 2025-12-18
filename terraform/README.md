# GCP Deployment with Terraform

GCP services used
-  a single `Cloud Run` service
    - Runs the container
    - exposes HTTPS
    - maps container port `8501` $\to$ `8080`


## Quickstart

Create a GCP service account with the following authorizations:
- `Cloud Run Developer`
    - `roles/run.developer`
    - create/update `Cloud Run` services
- `Service Account User` 
    - `roles/iam.serviceAccountUser`
    - attach runtime service account
- `Artifact Registry Writer` 
    - `roles/artifactregistry.writer`: 
    - push Docker image
- `Logs Writer`
    - `roles/logging.logWriter`
    - Useful for the container

Download and place the API key somewhere.
Create the `terraform.tfvars` on this folder:
```toml
project_id = "your project id"
region     = "your region"
service_name = "your service name"
```


```bash
terraform init
terraform apply
```