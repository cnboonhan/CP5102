#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

minikube stop --profile dev || true
minikube delete --profile dev || true

cd "$SCRIPT_DIR/idp"
docker-compose down -v
docker system prune
