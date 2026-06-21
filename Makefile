#!/usr/bin/env make -f
# -*- makefile -*-

SHELL = bash -e
VERSION_TYPE ?= patch
APP_NAME ?= agoras-actions
img_hash = $(shell docker images -q luisalejandro/agoras-actions:latest)
exec_on_docker = docker compose \
	-p agoras-actions -f docker-compose.yml exec -T \
	--user agoras app

lint: start
	@$(exec_on_docker) tox -e lint

format: start
	@$(exec_on_docker) bash -c 'pip install --quiet autopep8 && autopep8 --in-place --recursive --aggressive --aggressive docker'

test: start
	@$(exec_on_docker) tox -e coverage

# >>> rosey-maintainer:ops-docker BEGIN
# Managed by rosey-maintainer-tools 0.2.0. Do not edit directly.

PROJECT_NAME ?= agoras-actions
all_ps_hashes = $(shell docker ps -q)

image:
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml build \
		--build-arg UID=$(shell id -u) \
		--build-arg GID=$(shell id -g)

start:
	@if [ -z "$(img_hash)" ]; then\
		make image;\
	fi
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml up \
		--remove-orphans --no-build --detach

stop:
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml stop

down:
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml down \
		--remove-orphans

destroy:
	@echo
	@echo "WARNING!!!"
	@echo "This will stop and delete all containers, images and volumes related to this project."
	@echo
	@read -p "Press ctrl+c to abort or enter to continue." -n 1 -r
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml down \
		--rmi all --remove-orphans --volumes

cataplum:
	@echo
	@echo "WARNING!!!"
	@echo "This will stop and delete all containers, images and volumes present in your system."
	@echo
	@read -p "Press ctrl+c to abort or enter to continue." -n 1 -r
	@if [ -n "$(all_ps_hashes)" ]; then\
		docker kill $(shell docker ps -q);\
	fi
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml down \
		--rmi all --remove-orphans --volumes
	@docker system prune -a -f --volumes
# <<< rosey-maintainer:ops-docker END

console: start
	@$(exec_on_docker) bash

functional-test: start
	@$(exec_on_docker) bash test.sh

virtualenv: start
	@python3 -m venv --clear ./virtualenv
	@./virtualenv/bin/python3 -m pip install --upgrade pip
	@./virtualenv/bin/python3 -m pip install --upgrade setuptools
	@./virtualenv/bin/python3 -m pip install --upgrade wheel
	@./virtualenv/bin/python3 -m pip install "agoras==2.0.0"

docker-image:
	@docker build -f docker/Dockerfile \
		--build-arg VERSION=$$(grep '^current_version' .bumpversion.cfg | awk '{print $$3}') \
		--build-arg BUILD_DATE=$$(date -u +%Y-%m-%dT%H:%M:%SZ) \
		--build-arg VCS_REF=$$(git rev-parse --short HEAD 2>/dev/null || echo local) \
		-t luisalejandro/agoras-actions:latest \
		docker/

.PHONY: lint format test console functional-test virtualenv docker-image

# >>> rosey-maintainer:ops-release BEGIN
# Managed by rosey-maintainer-tools 0.2.0. Do not edit directly.

release:
	@./scripts/release.sh $${VERSION_TYPE}

release-patch:
	@./scripts/release.sh patch $${APP_NAME}

release-minor:
	@./scripts/release.sh minor $${APP_NAME}

release-major:
	@./scripts/release.sh major $${APP_NAME}


release-preflight: start


	@make lint

	@make format

	@make test



undo-release:
	@: "$${VERSION:?Set VERSION=x.y.z before running make undo-release}"
	@VERSION=$${VERSION} ./scripts/rollback.sh release
# <<< rosey-maintainer:ops-release END
