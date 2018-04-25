#!/bin/bash

set -e

EXTRA_ARGS="$@"

IMAGE="gonitro/${PWD##*/}"
TAG=$(git rev-parse --short HEAD)
IMAGE_NAME="${IMAGE}:${TAG}"

echo "Building Docker image ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" ${EXTRA_ARGS} .
[[ $? -eq 0 ]] && {
    docker tag "${IMAGE_NAME}" "${IMAGE}:latest"
    echo "Publishing ${IMAGE_NAME}"
    docker push "${IMAGE_NAME}"
    docker push "${IMAGE}:latest"
}
