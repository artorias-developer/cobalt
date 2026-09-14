export PYTHONPATH := $(shell pwd)/cobalt/backend

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
	docker compose --all-resources -f build/dev/docker-compose.yaml up -d
d\:b\:d: docker-build-dev

docker-rebuild-dev:
	docker compose --all-resources -f build/dev/docker-compose.yaml up -d --build
d\:r\:d: docker-rebuild-dev

docker-down-dev:
	docker compose -f build/dev/docker-compose.yaml down
d\:d\:d: docker-down-dev

docker-prune-dev:
	@read -p "This will remove all dev containers, volumes and images. Type 'y' to continue: " confirm; \
    if [ "$$confirm" != "y" ]; then \
		echo "Aborted."; \
		exit 1; \
	fi
	docker compose --all-resources -f build/dev/docker-compose.yaml down -v --rmi all --remove-orphans
d\:p\:d: docker-prune-dev

docker-build-prod:
	docker compose --all-resources -f build/prod/docker-compose.yaml up -d
d\:b\:p: docker-build-prod

docker-rebuild-prod:
	docker compose --all-resources -f build/prod/docker-compose.yaml up -d --build
d\:r\:p: docker-rebuild-prod

docker-down-prod:
	docker compose -f build/prod/docker-compose.yaml down
d\:d\:p: docker-down-prod

docker-prune-prod:
	@read -p "This will remove all prod containers, volumes and images. Type 'y' to continue: " confirm; \
    if [ "$$confirm" != "y" ]; then \
		echo "Aborted."; \
		exit 1; \
	fi
	docker compose --all-resources -f build/prod/docker-compose.yaml down -v --rmi all --remove-orphans
d\:p\:p: docker-prune-prod


alembic-init:
	alembic -c cobalt/backend/alembic.ini init -t async cobalt/backend/infrastructure/databases/postgres/migrations
a\:i: alembic-init

alembic-revision:
	alembic -c cobalt/backend/alembic.ini revision --autogenerate -m "$(name)"
a\:r: alembic-revision

alembic-upgrade:
	alembic -c cobalt/backend/alembic.ini upgrade head
a\:u: alembic-upgrade

alembic-downgrade:
	alembic -c cobalt/backend/alembic.ini downgrade -1
a\:d: alembic-downgrade

branches-local-delete:
	git branch | grep -v "dev\|main" | xargs git branch -D
b\:l\:d: branches-local-delete

locales-init:
	pybabel init -i cobalt/backend/infrastructure/locales/babel/messages.pot -d cobalt/backend/infrastructure/locales/babel -l $(locale)
l\:i: locales-init

locales-extract:
	mkdir -p cobalt/backend/infrastructure/locales/babel
	pybabel extract -F cobalt/backend/babel.cfg -o cobalt/backend/infrastructure/locales/babel/messages.pot cobalt/backend/ --no-wrap
l\:e: locales-extract

locales-update:
	pybabel update -i cobalt/backend/infrastructure/locales/babel/messages.pot -d cobalt/backend/infrastructure/locales/babel --no-wrap --no-fuzzy-matching --ignore-obsolete
l\:u: locales-update

locales-compile:
	pybabel compile -d cobalt/backend/infrastructure/locales/babel
l\:c: locales-compile