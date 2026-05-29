export PYTHONPATH := $(shell pwd)/cobalt/backend

.PHONY: \
    docker-build-dev d\:b\:d \
    docker-rebuild-dev d\:r\:d \
    docker-down-dev d\:d\:d \
    docker-build-prod d\:b\:p \
    docker-rebuild-prod d\:r\:p \
    docker-down-prod d\:d\:p \
    alembic-init a\:i \
    alembic-revision a\:r \
    alembic-upgrade a\:u \
    alembic-downgrade a\:d \
    delete-local-branches d\:l\:b

docker-build-dev:
	docker compose -f build/dev/docker-compose.yaml up -d
d\:b\:d: docker-build-dev

docker-rebuild-dev:
	docker compose -f build/dev/docker-compose.yaml up -d --build
d\:r\:d: docker-rebuild-dev

docker-down-dev:
	docker compose -f build/dev/docker-compose.yaml down
d\:d\:d: docker-down-dev

docker-build-prod:
	docker compose -f build/prod/docker-compose.yaml up -d
d\:b\:p: docker-build-prod

docker-rebuild-prod:
	docker compose -f build/prod/docker-compose.yaml up -d --build
d\:r\:p: docker-rebuild-prod

docker-down-prod:
	docker compose -f build/prod/docker-compose.yaml down
d\:d\:p: docker-down-prod

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

delete-local-branches:
	git branch | grep -v "dev\|main" | xargs git branch -D
d\:l\:b: delete-local-branches