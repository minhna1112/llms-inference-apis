IMAGE_NAME=$1

docker build -t ${IMAGE_NAME} -f build/docker/client.dockerfile .