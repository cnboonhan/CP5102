#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

minikube stop --profile dev || true
minikube delete --profile dev || true

cd "$SCRIPT_DIR/docker"
docker-compose down

docker system prune

rm "$SCRIPT_DIR/docker/keycloak/realms.json" || true
rm -r "$SCRIPT_DIR/docker/keycloak/stores" || true
rm -r "$SCRIPT_DIR/docker/reverseproxy/certs" || true
