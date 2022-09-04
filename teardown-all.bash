#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

minikube stop --profile dev
minikube delete --profile dev

cd "$SCRIPT_DIR/docker"
docker-compose down

docker system prune
