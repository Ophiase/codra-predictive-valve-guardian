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
	echo "TODO..."

dashboard_docker:
	echo "TODO..."
	