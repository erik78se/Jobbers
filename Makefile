# VARIABLES

# TARGETS
lint: ## Run linter
	tox -e lint

smoke-test: build ## Run smoke tests
	tox -e smoke

integration-test: build ## Run integration tests
	tox -e integration

build: clean ## build python package
	tox -e build

snap: clean-snap ## build snap (make snap SNAPCRAFT_BUILD_ENVIRONMENT=lxd|kvm)
	snapcraft

push: build ## TODO: Push to artifactory edge channels
	echo "No pushing yet"

clean: ## Remove .tox and build dirs
	rm -rf build/ dist/ .tox/

clean-snap: ## snapcraft clean
	snapcraft clean

# Display target comments in 'make help'
help: 
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# SETTINGS
# Use one shell for all commands in a target recipe
.ONESHELL:
# Set default goal
.DEFAULT_GOAL := help
# Use bash shell in Make instead of sh 
SHELL := /bin/bash
