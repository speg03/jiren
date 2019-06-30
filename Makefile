.PHONY: test build publish

test:
	poetry run pytest -v --cov=jiren/ --cov-report=term-missing tests/

build:
	poetry build

publish: build
	poetry publish
