#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

minikube stop --profile dev || true
minikube delete --profile dev || true

cd "$SCRIPT_DIR/external_infra"
docker-compose down -v
docker system prune -f

cd "$SCRIPT_DIR/red_team"
rm -r .iac || true
rm -r .out || true
