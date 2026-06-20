#!/usr/bin/env make -f
# -*- makefile -*-

SHELL = bash -e
img_hash = $(shell docker images -q luisalejandro/agoras-actions:latest)
exec_on_docker = docker compose \
	-p agoras-actions -f docker-compose.yml exec \
	--user agoras app

# >>> rosey-maintainer:ops-docker BEGIN
# Managed by rosey-maintainer-tools. Do not edit directly.

PROJECT_NAME ?= agoras-actions
all_ps_hashes = $(shell docker ps -q)

image:
	@docker compose -p $(PROJECT_NAME) -f docker-compose.yml build \
		--build-arg UID=$(shell id -u) \
		--build-arg GID=$(shell id -g)

docker-image:
	@docker buildx build \
		-f docker/Dockerfile \
		docker \
		-t ghcr.io/luisalejandro/agoras-actions:1.1.3 \
		--load

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
	@./virtualenv/bin/python3 -m pip install "agoras==1.1.3"