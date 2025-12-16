IMAGE=valve-guardian-dashboard
CONTAINER=valve-guardian-dashboard

sync:
	uv sync

retrieve_data:
	uv run -m processor.data.retrieve_data

test_model:
	uv run -m processor.tests.verify_model

train_model:
	uv run -m processor.train.train_model

model_estimation:
	uv run -m processor.model.estimate_model

dashboard:
	PYTHONPATH=. uv run streamlit run dashboard/app.py \
		--server.port=8501 \
		--server.address=0.0.0.0

build_dashboard:
	docker build -t $(IMAGE) .

dashboard_docker_run: build_dashboard
	docker run --name $(CONTAINER) -p 8501:8501 $(IMAGE)

dashboard_docker:
	if [ "$(shell docker ps -aq -f name=^$(CONTAINER)$$)" ]; then \
		docker start -ai $(CONTAINER); \
	else \
		$(MAKE) dashboard_docker_run; \
	fi
	
.PHONY: sync retrieve_data test_model train_model model_estimation dashboard build_dashboard dashboard_docker dashboard_docker_run