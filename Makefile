.PHONY: all db transform build validate publish

EXT = yaml
INPUT_DIR = data-raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
DB_FILES := $(addsuffix /db.sqlite,$(addprefix $(INPUT_DIR)/,$(RESOURCE_NAMES)))

all: transform build validate

db: $(DB_FILES)

data-raw/%/db.sqlite: data-raw/%/*.yaml
	python main.py transform $*

build: transform
	python main.py build $(OUTPUT_DIR)

validate: 
	frictionless validate datapackage.yaml

publish: 
	git add -Af $(OUTPUT_DIR)/*.csv $(INPUT_DIR)/*.$(EXT) $(OUTPUT_DIR)/datapackage.json
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package at: $$(date +%Y-%m-%dT%H:%M:%SZ)" || exit 0
	git push

print:
	@echo $(DB_FILES)