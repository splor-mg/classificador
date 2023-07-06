.PHONY: all transform build validate publish

EXT = yaml
INPUT_DIR = data-raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)

all: transform build validate

transform: db.sqlite

db.sqlite: data-raw/*/*.yaml
	python main.py transform $*

build: transform
	python main.py build $(OUTPUT_DIR)

validate: 
	frictionless validate datapackage.yaml

publish: 
	git add -Af $(OUTPUT_DIR)/*.csv $(INPUT_DIR)/*.$(EXT) $(OUTPUT_DIR)/datapackage.json
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package at: $$(date +%Y-%m-%dT%H:%M:%SZ)" || exit 0
	git push
