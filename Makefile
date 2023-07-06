.PHONY: all db transform build validate

EXT = sqlite
INPUT_DIR = data-raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix $(OUTPUT_DIR)/,$(RESOURCE_NAMES)))
DB_FILES := $(addsuffix /db.sqlite,$(addprefix $(INPUT_DIR)/,$(RESOURCE_NAMES)))

all: extract transform build validate

extract: $(DB_FILES)

data-raw/%/db.sqlite: data-raw/%/*.yaml
	python main.py extract $*

transform: $(OUTPUT_FILES)

$(OUTPUT_FILES): $(OUTPUT_DIR)/%.csv: $(INPUT_DIR)/%/db.$(EXT) schema.yaml scripts/transform.py datapackage.yaml
	python main.py transform $* $@

build: transform
	python main.py build $(OUTPUT_DIR)

validate: 
	frictionless validate datapackage.yaml
