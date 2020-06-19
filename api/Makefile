.PHONY: test
PROJECT_NAME:=ANIBOV
container:=${container}
environment?=staging


PYTHON3=/usr/bin/env python3


test:
	@pytest

api:
	@python3 bin/api.py



build: ; @\
        clear; \
        echo "[Building Environment...]"; \
        echo "";\
        docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} up --build --remove-orphans -d

start: ; @\
        clear; \
        echo "[Starting Environment: "${environment}"...]"; \
        echo ""; \
        docker-compose -f docker/docker-compose.yml -f docker/docker-compose.${environment}.yml -p ${PROJECT_NAME} up ${container}

stop: ; @\
        clear; \
        echo "[Stopping Environment...]"; \
        echo "";\
        docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} down | true

status: ; @\
        clear; \
        echo "[Status...]"; \
        echo "";\
        docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} ps

clean: ; @\
        clear; \
        echo "[Cleaning Dangling images...]"; \
        echo "";\
        docker rmi -f `docker images -q -f dangling=true`; \
        echo "";\
        echo "[Cleaning Dangling volumes...]"; \
        echo "";\
        docker volume rm `docker volume ls -q -f dangling=true`

logs: ; @\
        clear; \
        echo "[Generating logs...]"; \
        echo "";\
        docker-compose -f docker/docker-compose.yml logs -f

