#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MINIKUBE_IS_SET_UP="$(minikube profile | grep dev || true)"
KICS_DOCKER_IMAGE_IS_PULLED="$(docker images -q checkmarx/kics)"
[[ -n "$KICS_DOCKER_IMAGE_IS_PULLED" ]] || docker pull checkmarx/kics:latest
[[ -n "$MINIKUBE_IS_SET_UP" ]] || ( minikube start --profile dev && minikube profile dev && minikube addons enable ingress && skaffold config set --global local-cluster true )

mkdir -p "$SCRIPT_DIR/certs"
openssl s_client -showcerts -connect "$(minikube ip):443" </dev/null |  sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > "$SCRIPT_DIR/certs/ingress-cert.pem"
openssl x509 -pubkey -noout -in "$SCRIPT_DIR/certs/ingress-cert.pem"  > "$SCRIPT_DIR/certs/ingress-pubkey.pem"

cd "$SCRIPT_DIR/docker"
docker-compose down
docker-compose up --build reverseproxy --build mockpass -d

cd "$SCRIPT_DIR"
[[ -x "$SCRIPT_DIR/pre-deploy-exec.bash" ]] || chmod +x pre-deploy-exec.bash
skaffold dev
