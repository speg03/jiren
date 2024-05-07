.PHONY: all
all: dist

.PHONY: clean
clean:
	rm -rf ./dist

.PHONY: requirements
requirements:
	uv pip compile -U pyproject.toml -o requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v ./tests

.PHONY: dist
dist:
	python3 -m build
