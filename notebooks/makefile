SOURCE_DIR = src
OUTPUT_DIR = ../docs/10-Tutorials

SOURCES = $(wildcard $(SOURCE_DIR)/*.py)

NOTEBOOKS = \
	$(patsubst $(SOURCE_DIR)/%.py,$(OUTPUT_DIR)/%.ipynb,$(SOURCES)) \
	$(patsubst $(SOURCE_DIR)/%.py,$(OUTPUT_DIR)/%_students.ipynb,$(SOURCES))

.DEFAULT_GOAL := all

$(SOURCE_DIR)/%_students.py: $(SOURCE_DIR)/%.py
	sed -e 's/^\(\ *\).*REMOVED.*$$/\1*** FILL THE MISSING LINE ***/g' \
		-e 's/^\(#\ #\ .*\)$$/\1 \(students version\)/g' $< > $@

$(OUTPUT_DIR)/%.ipynb: $(SOURCE_DIR)/%.py
	jupytext --to ipynb --output $@ $< 

.PHONY: clean
clean:
	rm $(OUTPUT_DIR)/*.ipynb

.PHONY: all
all: $(NOTEBOOKS)
