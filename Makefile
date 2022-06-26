.PHONY: all clean build lint test

all: build

clean:
	rm -rf ./dist

build: lint test
	poetry build

lint:
	pre-commit run --all-files

test:
	pytest -v ./tests
