.PHONY: integration-tests

VENV := .venv
PYTHON := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PYTEST := $(PYTHON) -m pytest
PYTEST_ARGS ?= -q

$(VENV)/bin/python:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi
	@"$(VENV)/bin/python" -m pip install -q --upgrade pip || true

integration-tests: $(VENV)/bin/python
	@if [ -x "$(VENV)/bin/python" ]; then \
		"$(VENV)/bin/python" -m pip install -q pytest || true; \
	else \
		python3 -m pip install --user -q pytest || true; \
	fi
	$(PYTEST) $(PYTEST_ARGS) integration-tests | cat

.PHONY: integration-tests-verbose
integration-tests-verbose: PYTEST_ARGS=-s -vv -rP --log-cli-level=INFO
integration-tests-verbose: integration-tests

.PHONY: generate
TEMPLATE_IDS := $(patsubst new-template-form-inputs/%.md,%,$(wildcard new-template-form-inputs/*.md))

generate:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make generate <template-id>"; \
		echo "Available: $(TEMPLATE_IDS)"; \
		exit 1; \
	fi

.PHONY: $(TEMPLATE_IDS)
$(TEMPLATE_IDS):
	@name=$@; \
	input="new-template-form-inputs/$$name.md"; \
	rm -rf generated-templates/$$name; \
	mkdir -p generated-templates/$$name; \
	CLAUDE_CODE_MAX_OUTPUT_TOKENS=16384 sf ai claude -- --dangerously-skip-permissions -p "Follow instructions from prompts/new-template-generation.md to generate a new template (template id: $$name) for the user inputs in $$input" --verbose --output-format stream-json | tee generated-templates/$$name/claude-output.json

