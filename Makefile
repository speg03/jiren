.PHONY: all clean build lint test

all: build
clean:
	rm -rf ./dist

lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
build:
	python3 -m pip install build
	python3 -m build
