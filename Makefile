PROJECT_NAME:=systemlake
container:=${container}

help: ; @ \
	clear; \
	echo ""; \
	echo "Usage instructions:"; \
	echo ""; \
	echo 'make build: \tCreate new development environment'; \
	echo 'make start: \tStart development environment previously created'; \
	echo 'make stop: \tStop development environment'; \
	echo 'make status: \tShow development environment'; \
	echo 'make restart: \tRestart development environment'; \
	echo 'make logs \tShow development environment logs'; \
	echo 'make clean \tClean dangling volume and images from docker'; \
	echo "make help: \tHow to use make command";\
	echo "";

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
