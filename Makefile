FILE=VERSION
PROJ_VERSION:=`cat $(FILE)`
CLIENT_IMAGE = "your_registry/tgi_client"



run_server:
	bash scripts/run_server.sh

build_client:
	bash scripts/build_client.sh ${CLIENT_IMAGE}:${PROJ_VERSION}

run_client:
	bash scripts/run_client.sh ${CLIENT_IMAGE}:${PROJ_VERSION}

push_client:
	docker push ${CLIENT_IMAGE}:${PROJ_VERSION}

run_all:
	docker compose up

push_all:
	make push_client
