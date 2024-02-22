.PHONY: all
all: dist

.PHONY: clean
clean:
	rm -rf ./dist

.PHONY: requirements
requirements:
	pip-compile --upgrade --output-file=./requirements.txt ./pyproject.toml

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v ./tests

.PHONY: dist
dist:
	python3 -m build
