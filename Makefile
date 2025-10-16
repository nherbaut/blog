# Usage: make "Custom Title" https://doi.org/10.xxx/yyy
TITLE := $(firstword $(MAKECMDGOALS))
DOI   := $(word 2,$(MAKECMDGOALS))

.PHONY: % help
%:
	@if [ "$@" = "$(TITLE)" ]; then \
	  if [ -z "$(TITLE)" ] || [ -z "$(DOI)" ]; then echo "Usage: make \"Custom Title\" https://doi.org/10.xxxx"; exit 2; fi; \
	  python3 scripts/openalex_to_hugo.py "$(TITLE)" "$(DOI)"; \
	fi

help:
	@echo 'Usage: make "Custom Title" https://doi.org/10.xxxx'

