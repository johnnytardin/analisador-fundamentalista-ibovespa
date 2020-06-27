PROJECT_NAME:=analisador
container:=${container}

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
	docker-compose  -p ${PROJECT_NAME} up -d ${container}

scrap: ; @\
	clear; \
	echo "[Starting Environment and scraping...]"; \
	echo ""; \
	docker-compose -f docker-compose-scrap.yml -p ${PROJECT_NAME} up -d ${container}

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
