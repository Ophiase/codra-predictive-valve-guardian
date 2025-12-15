sync:
	uv sync

retrieve_data:
	uv run -m data.retrieve_data

test_model:
	uv run -m model.test_model

train_model:
	uv run -m train.train_model

model_estimation:
	uv run -m model.estimate_model