.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "HA available targets:"
	@echo ""
	@grep -E '^.PHONY:.*##.*' $(MAKEFILE_LIST) | cut -c9- | sort | awk 'BEGIN {FS = " ## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: upgrade ## Upgrade HA Docker to the latest version
upgrade:
	docker-compose pull && docker-compose down && docker-compose up -d

.PHONY: update-custom-ui ## Update CustomUI to the latest version
update-custom-ui:
	cd ./config; bash ./update.sh
