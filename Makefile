.PHONY: all clean build lint test

all: build
clean:
	rm -rf ./dist

lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
build: lint test
	poetry build