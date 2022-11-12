SOURCE_DIR = src
OUTPUT_DIR = build

SOURCES = $(wildcard $(SOURCE_DIR)/*.py)

NOTEBOOKS = \
	$(patsubst $(SOURCE_DIR)/%.py,$(OUTPUT_DIR)/%.ipynb,$(SOURCES)) \
	$(patsubst $(SOURCE_DIR)/%.py,$(OUTPUT_DIR)/%_students.ipynb,$(SOURCES))

$(SOURCE_DIR)/%_students.py: $(SOURCE_DIR)/%.py
	sed 's/^\(\ *\).*LINE TO BE REMOVED FOR STUDENTS.*$$/\1*** FILL THE MISSING LINE ***/g' \
		$< > $@

$(OUTPUT_DIR)/%.ipynb: $(SOURCE_DIR)/%.py
	jupytext --to ipynb --output $@ $< 

.PHONY: clean
clean:
	rm $(OUTPUT_DIR)/*.ipynb

.PHONY: all
all: $(NOTEBOOKS)
