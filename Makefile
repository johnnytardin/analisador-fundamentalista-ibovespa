PROJECT_NAME:=analisador
container:=${container}

clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

enable-dev:
	@cp dev.env .env

enable-local:
	@cp local.env .env

test:
	poetry run pytest -sx

check-dead-fixtures:
	poetry run pytest --dead-fixtures

lint:
	poetry install && poetry run -a -v

pyformat:
	poetry run isort . && poetry run black .


build: ; @\
	clear; \
	echo "[Building Environment...]"; \
	echo "";\
	docker-compose down ; \
	docker-compose  -p ${PROJECT_NAME} up --build --remove-orphans -d ${container}; \
	docker-compose down

start: ; @\
	clear; \
	echo "[Starting Environment...]"; \
	echo ""; \
	docker-compose -p ${PROJECT_NAME} up -d ${container}

scrap: ; @\
	clear; \
	echo "[Starting Environment and scraping...]"; \
	echo ""; \
	docker-compose -f docker-compose-scrap.yml -p ${PROJECT_NAME} up -d ${container} --build

stop: ; @\
	clear; \
	echo "[Stopping Environment...]"; \
	echo "";\
	docker-compose  -p ${PROJECT_NAME} down

status: ; @\
	clear; \
	echo "[Status...]"; \
	echo "";\
	docker-compose -p ${PROJECT_NAME} ps

clean: ; @\
	clear; \
	echo "[Cleaning Dangling images...]"; \
	echo "";\
	docker rmi -f `docker images -q -f dangling=true`; \
	echo "";\
	echo "[Cleaning Dangling volumes...]"; \
	echo "";\
	docker volume rm `docker volume ls -q -f dangling=true`

restart: stop start

logs: ; @\
	clear; \
	echo "[Generating environment logs...]"; \
	echo "";\
	docker-compose -p ${PROJECT_NAME} logs -f
