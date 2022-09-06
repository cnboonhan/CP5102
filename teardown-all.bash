#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

minikube stop --profile dev
minikube delete --profile dev

cd "$SCRIPT_DIR/docker"
docker-compose down

docker system prune

rm "$SCRIPT_DIR/keycloak/realms.json" || true
rm -r "$SCRIPT_DIR/keycloak/stores" || true
rm -r "$SCRIPT_DIR/reverseproxy/certs" || true
