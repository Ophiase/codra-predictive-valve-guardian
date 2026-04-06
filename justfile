set dotenv-load := true
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# User

[group("USER")]
install:
    uv run task install

[group("USER")]
uninstall:
    rm -rf .venv

[group("USER")]
reinstall:
    rm -rf .venv
    uv run task install

[group("USER")]
dashboard:
    uv run streamlit run src/dashboard/__main__.py \
    	--server.port=8501 \
    	--server.address=0.0.0.0

[group("USER")]
start: dashboard

# Dev

[group("AI")]
retrieve_data:
    uv run -m processor.data.retrieve_data

[group("AI")]
train_model:
    uv run -m processor.train

[group("AI")]
model_estimation:
    uv run -m processor.train.model_estimation

[group("TEST")]
tests:
    @echo "Running all tests..."

[group("DEMO")]
demo:
    uv run -m tests.demo.verify_data
    uv run -m tests.demo.verify_model

[group("DEV")]
update:
    @uv run task update

[group("DEV")]
enable_hooks:
    uv run pre-commit install

[group("DEV")]
disable_hooks:
    uv run pre-commit uninstall

[group("DEV")]
lint:
    @uv run task lint

[group("DEV")]
ty:
    @uv run task ty

[group("DEV")]
precommit:
    uv run task lint
    uv run task ty

# deploy

DEV_TAG := "dev"
LATEST_TAG := "latest"
IMAGE_NAME := "valve-guardian-dashboard"
CONTAINER_NAME := "valve-guardian-dashboard"

[group("DEPLOY")]
build tag=DEV_TAG:
    docker build -t {{ CONTAINER_NAME }}:{{ tag }} .

[group("UTILITIES")]
_increment:
    @echo "Incrementing version..."

[group("UTILITIES")]
[script("bash")]
_tag version is_latest="true":
    docker tag \
        {{ IMAGE_NAME }}:{{ DEV_TAG }} \
        {{ IMAGE_NAME }}:{{ version }}
    if [ "{{ is_latest }}" = "true" ]; then \
        docker tag \
            {{ IMAGE_NAME }}:{{ DEV_TAG }} \
            {{ IMAGE_NAME }}:latest; \
    fi

[group("DEPLOY")]
run tag=DEV_TAG:
    docker run --name {{ CONTAINER_NAME }} -p 8501:8501 {{ IMAGE_NAME }}:{{ tag }}

[group("DEPLOY")]
release:
    @echo "Releasing new version..."
