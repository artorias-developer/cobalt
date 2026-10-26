export PYTHONPATH := $(shell pwd)/cobalt/backend

BACKEND_DIR        := cobalt/backend
COMPOSE_DEV        := build/dev/docker-compose.yml
COMPOSE_PROD       := build/prod/docker-compose.yml
ALEMBIC_INI        := $(BACKEND_DIR)/alembic.ini
ALEMBIC_MIGRATIONS := $(BACKEND_DIR)/infrastructure/databases/postgres/migrations
BABEL_CFG          := $(BACKEND_DIR)/babel.cfg
LOCALES_DIR        := $(BACKEND_DIR)/infrastructure/locales/babel
LOCALES_POT        := $(LOCALES_DIR)/messages.pot

.PHONY: \
	docker-build-dev d\:b\:d \
	docker-rebuild-dev d\:r\:d \
	docker-down-dev d\:d\:d \
	docker-prune-dev d\:p\:d \
	docker-build-prod d\:b\:p \
	docker-rebuild-prod d\:r\:p \
	docker-down-prod d\:d\:p \
	docker-prune-prod d\:p\:p \
	alembic-init a\:i \
	alembic-revision a\:r \
	alembic-upgrade a\:u \
	alembic-downgrade a\:d \
	branches-local-delete b\:l\:d \
	locales-init l\:i \
	locales-extract l\:e \
	locales-update l\:u \
	locales-compile l\:c

docker-build-dev:
	docker compose --all-resources -f $(COMPOSE_DEV) up -d
d\:b\:d: docker-build-dev

docker-rebuild-dev:
	docker compose --all-resources -f $(COMPOSE_DEV) up -d --build
d\:r\:d: docker-rebuild-dev

docker-down-dev:
	docker compose -f $(COMPOSE_DEV) down
d\:d\:d: docker-down-dev

docker-prune-dev:
	@read -p "This will remove all dev containers, volumes and images. Type 'y' to continue: " confirm; \
	if [ "$$confirm" != "y" ]; then \
	   echo "Aborted."; \
	   exit 1; \
	fi
	docker compose --all-resources -f $(COMPOSE_DEV) down -v --rmi all --remove-orphans
d\:p\:d: docker-prune-dev

docker-build-prod:
	docker compose --all-resources -f $(COMPOSE_PROD) up -d
d\:b\:p: docker-build-prod

docker-rebuild-prod:
	docker compose --all-resources -f $(COMPOSE_PROD) up -d --build
d\:r\:p: docker-rebuild-prod

docker-down-prod:
	docker compose -f $(COMPOSE_PROD) down
d\:d\:p: docker-down-prod

docker-prune-prod:
	@read -p "This will remove all prod containers, volumes and images. Type 'y' to continue: " confirm; \
	if [ "$$confirm" != "y" ]; then \
	   echo "Aborted."; \
	   exit 1; \
	fi
	docker compose --all-resources -f $(COMPOSE_PROD) down -v --rmi all --remove-orphans
d\:p\:p: docker-prune-prod


alembic-init:
	alembic -c $(ALEMBIC_INI) init -t async $(ALEMBIC_MIGRATIONS)
a\:i: alembic-init

alembic-revision:
	alembic -c $(ALEMBIC_INI) revision --autogenerate -m "$(name)"
a\:r: alembic-revision

alembic-upgrade:
	alembic -c $(ALEMBIC_INI) upgrade head
a\:u: alembic-upgrade

alembic-downgrade:
	alembic -c $(ALEMBIC_INI) downgrade -1
a\:d: alembic-downgrade

branches-local-delete:
	git branch | grep -v "dev\|main" | xargs git branch -D
b\:l\:d: branches-local-delete

locales-init:
	pybabel init -i $(LOCALES_POT) -d $(LOCALES_DIR) -l $(locale)
l\:i: locales-init

locales-extract:
	mkdir -p $(LOCALES_DIR)
	pybabel extract -F $(BABEL_CFG) -o $(LOCALES_POT) $(BACKEND_DIR)/ --no-wrap
l\:e: locales-extract

locales-update:
	pybabel update -i $(LOCALES_POT) -d $(LOCALES_DIR) --no-wrap --no-fuzzy-matching --ignore-obsolete
l\:u: locales-update

locales-compile:
	pybabel compile -d $(LOCALES_DIR)
l\:c: locales-compile