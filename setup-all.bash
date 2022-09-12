#!/bin/bash
set -e
set -o xtrace

# Name of network here is coupled with naming in docker-compose.yaml
get_keycloak_idp_ip(){
docker network inspect idp_network  | \
  jq '.[] | select(.Name=="idp_network")' | \
  jq '.Containers' | \
  jq '.[] | select(.Name=="keycloak-idp")' | \
  jq '.IPv4Address' | \
  grep -oE '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])'
}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MINIKUBE_IS_SET_UP="$(minikube profile | grep dev || true)"
KICS_DOCKER_IMAGE_IS_PULLED="$(docker images -q checkmarx/kics)"
KEYCLOAK_IDP_HOST="${KEYCLOAK_IDP_HOST:-192.168.49.1}"

[[ -n "$KICS_DOCKER_IMAGE_IS_PULLED" ]] || docker pull checkmarx/kics:latest
[[ -n "$MINIKUBE_IS_SET_UP" ]] || ( minikube start --profile dev && minikube profile dev && minikube addons enable ingress && skaffold config set --global local-cluster true )

cd "$SCRIPT_DIR/idp"
docker-compose down
docker-compose up --build -d

until [ -n "$(get_keycloak_idp_ip)" ]
do
  echo "Waiting for Keycloak IP Address to be assigned.."
  sleep 2
done

until [ -n "$(minikube ip)" ]
do
  echo "Waiting for minikube ingress ip to be up.."
  sleep 2
done

[[ -x "$SCRIPT_DIR/pre-deploy-exec.bash" ]] || chmod +x pre-deploy-exec.bash

cd "$SCRIPT_DIR"
KEYCLOAK_IDP_HOST=$KEYCLOAK_IDP_HOST MINIKUBE_INGRESS_HOST=$(minikube ip) skaffold dev
