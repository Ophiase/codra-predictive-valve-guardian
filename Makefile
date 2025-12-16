IMAGE=valve-guardian-dashboard
CONTAINER=valve-guardian-dashboard

###########################################################

# Quick run
dashboard:
	PYTHONPATH=. uv run streamlit run dashboard/app.py \
		--server.port=8501 \
		--server.address=0.0.0.0

build_dashboard:
	docker build -t $(IMAGE) .

dashboard_docker_run: build_dashboard
	docker run --name $(CONTAINER) -p 8501:8501 $(IMAGE)

# Quick run (Dockerized)
dashboard_docker:
	if [ "$(shell docker ps -aq -f name=^$(CONTAINER)$$)" ]; then \
		docker start -ai $(CONTAINER); \
	else \
		$(MAKE) dashboard_docker_run; \
	fi

###########################################################

sync:
	uv sync

retrieve_data:
	uv run -m processor.data.retrieve_data

tests: # TODO: use unit test framework
	uv run -m processor.tests.verify_data
	uv run -m processor.tests.verify_model

train_model:
	uv run -m processor.train.train_model

model_estimation:
	uv run -m processor.train.model_estimation


###########################################################
# Development environment setup and utilities
###########################################################

dev_setup:
	uv sync --group dev
# 	uv run pre-commit install

enable_hooks:
	uv run pre-commit install
disable_hooks:
	uv run pre-commit uninstall

format:
	uv run black .
	uv run isort .

###########################################################
	
.PHONY: sync retrieve_data test_model train_model model_estimation dashboard build_dashboard dashboard_docker dashboard_docker_run
