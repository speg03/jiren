.PHONY: all clean requirements dist lint test

all: dist
clean:
	rm -rf ./dist

requirements:
	pip-compile --upgrade --output-file=./requirements.txt ./pyproject.toml
lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
dist:
	python3 -m build
