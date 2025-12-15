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
	docker build -t valve-guardian-dashboard .

dashboard_docker:
	docker build -t valve-guardian-dashboard .
	docker run -p 8501:8501 valve-guardian-dashboard
	
.PHONY: sync retrieve_data test_model train_model model_estimation dashboard build_dashboard dashboard_docker