.PHONY: all prepare benchmark metrics leaderboard report clean test install

install:
	pip install -r requirements.txt

all: prepare benchmark metrics leaderboard report

prepare:
	python scripts/prepare_dataset.py

benchmark:
	python scripts/run_benchmark.py --model all

benchmark-mock:
	python scripts/run_benchmark.py --model mock

benchmark-model:
	python scripts/run_benchmark.py --model $(MODEL)

metrics:
	python scripts/calculate_metrics.py

leaderboard:
	python scripts/generate_leaderboard.py

report:
	python scripts/generate_report.py

test:
	pytest tests/ -v

clean:
	find . -type f -name '*.pyc' -delete
	rm -rf results/raw results/metrics results/leaderboards evidence/errors
	mkdir -p results/raw results/metrics results/leaderboards evidence/errors
