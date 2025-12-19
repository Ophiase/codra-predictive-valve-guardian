# GCP Deployment with Terraform

GCP services used
-  a single `Cloud Run` service
    - Runs the container
    - exposes HTTPS
    - maps container port `8501` $\to$ `8080`


## Instructions

0. Enable Cloud Run and Artifact Registry APIs on your GCP project.

1. Create a GCP service account with the following authorizations:
- `Cloud Run Developer`
    - `roles/run.developer`
    - create/update `Cloud Run` services
- `Service Account User` 
    - `roles/iam.serviceAccountUser`
    - attach runtime service account
- ⚠️ `Artifact Registry Admin`
    - `roles/artifactregistry.admin`
    - create Artifact Registry repo
    - ⚠️ only needed if the repo does not exist yet
    - ⚠️ recommended to remove this role after the repo is created
- `Artifact Registry Writer` 
    - `roles/artifactregistry.writer`: 
    - push Docker image
- `Logs Writer`
    - `roles/logging.logWriter`
    - Useful for the container

2. Download and place the API key somewhere.
3. Build the dashboard image
```bash
cd ..
make build_dashboard
```
4. Upload the dashboard image to Artifact Registry
```bash
# Connect to your service account
GOOGLE_APPLICATION_CREDENTIALS="<insert keyfile path>.json"
gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"

# Set project and region variables
PROJECT_ID="<your-gcp-project>"
GCP_REGION="europe-west9"  # choose a specific region, not "EU"
REPO_NAME="predictive-valve-guardian-dashboard"
IMAGE_NAME="valve-guardian-dashboard"
IMAGE_TAG="latest"

# Create Artifact Registry repo (run only once)
gcloud artifacts repositories create $REPO_NAME \
  --repository-format=docker \
  --location=$GCP_REGION \
  --description="Private Cloud Run demo docker repo" \
  --project=$PROJECT_ID || echo "Repo already exists, skipping"

# Configure Docker to authenticate with Artifact Registry
gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev

# Tag the local image with the Artifact Registry path
docker tag ${IMAGE_NAME}:latest \
  ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}


# Push the image to Artifact Registry
docker push ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}
```

3. Create the `terraform.tfvars` on this folder:
```toml
project_id = "<your-gcp-project-id>"
region = "<your-gcp-region>" # e.g. europe-west9
service_name = "predictive-valve-guardian-service"
image = "<your-gcp-region>-docker.pkg.dev/<your-gcp-project-id>/predictive-valve-guardian-dashboard/valve-guardian-dashboard:latest"
credentials_path="<path-to-your-service-account-key>.json"
```

4. Run Terraform:

```bash
terraform init
terraform apply
```