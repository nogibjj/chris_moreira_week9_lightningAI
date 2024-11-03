install:
	pip install --upgrade pip && pip install -r requirements.txt

test:
	python -m pytest -vv --nbval --cov=mylib --cov=main *.py test_*.py *.ipynb

format:
	nbqa black *.ipynb && black *.py && black test_*.py

lint:
	ruff check test_*.py && ruff check *.py --fix
	nbqa ruff *.ipynb --fix

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	# Deploy command goes here

all: install test format lint deploy
