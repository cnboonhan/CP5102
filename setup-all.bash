#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MINIKUBE_IS_SET_UP="$(minikube profile | grep dev || true)"
KICS_DOCKER_IMAGE_IS_PULLED="$(docker images -q checkmarx/kics)"
[[ -n "$KICS_DOCKER_IMAGE_IS_PULLED" ]] || docker pull checkmarx/kics:latest
[[ -n "$MINIKUBE_IS_SET_UP" ]] || ( minikube start --profile dev && minikube profile dev && minikube addons enable ingress && skaffold config set --global local-cluster true )

KEYCLOAK_TRUSTSTORE_PATH="$SCRIPT_DIR/docker/keycloak/keycloak-truststore.p12"
MINIKUBE_CERT_PATH="$SCRIPT_DIR/docker/mockpass/certs"
NGINX_CERT_PATH="$SCRIPT_DIR/docker/reverseproxy"

mkdir -p "$MINIKUBE_CERT_PATH"
openssl s_client -showcerts -connect "$(minikube ip):443" </dev/null |  sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > "$MINIKUBE_CERT_PATH/ingress-cert.pem"
openssl x509 -pubkey -noout -in "$MINIKUBE_CERT_PATH/ingress-cert.pem"  > "$MINIKUBE_CERT_PATH/ingress-pubkey.pem"

keytool -importcert -storetype PKCS12 -keystore "$KEYCLOAK_TRUSTSTORE_PATH" -storepass changeit -alias minikube -file "$NGINX_CERT_PATH/nginx-selfsigned.crt" -noprompt

cd "$SCRIPT_DIR/docker"
docker-compose down
docker-compose up --build reverseproxy --build mockpass -d

cd "$SCRIPT_DIR"
[[ -x "$SCRIPT_DIR/pre-deploy-exec.bash" ]] || chmod +x pre-deploy-exec.bash
skaffold dev
