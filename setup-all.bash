#!/bin/bash
set -e
set -o xtrace

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MINIKUBE_IS_SET_UP="$(minikube profile | grep dev || true)"
KICS_DOCKER_IMAGE_IS_PULLED="$(docker images -q checkmarx/kics)"
[[ -n "$KICS_DOCKER_IMAGE_IS_PULLED" ]] || docker pull checkmarx/kics:latest
[[ -n "$MINIKUBE_IS_SET_UP" ]] || ( minikube start --profile dev && minikube profile dev && minikube addons enable ingress && skaffold config set --global local-cluster true )

KEYCLOAK_STORE_PATH="$SCRIPT_DIR/docker/keycloak/stores"
MINIKUBE_CERT_PATH="$SCRIPT_DIR/docker/mockpass/certs"
NGINX_CERT_PATH="$SCRIPT_DIR/docker/reverseproxy/certs"

mkdir -p "$MINIKUBE_CERT_PATH"
openssl s_client -showcerts -connect "$(minikube ip):443" </dev/null |  sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > "$MINIKUBE_CERT_PATH/ingress-cert.pem"
openssl x509 -pubkey -noout -in "$MINIKUBE_CERT_PATH/ingress-cert.pem"  > "$MINIKUBE_CERT_PATH/ingress-pubkey.pem"

mkdir -p "$NGINX_CERT_PATH"
openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=*" -addext "subjectAltName=DNS:localhost,IP:192.168.49.1" -newkey rsa:2048 -keyout "$NGINX_CERT_PATH/nginx-selfsigned.key" -out "$NGINX_CERT_PATH/nginx-selfsigned.crt"

mkdir -p $KEYCLOAK_STORE_PATH
rm -f "$KEYCLOAK_STORE_PATH/keycloak-truststore.p12" 
keytool -importcert -storetype PKCS12 -keystore "$KEYCLOAK_STORE_PATH/keycloak-truststore.p12" -storepass changeit -alias minikube -file "$NGINX_CERT_PATH/nginx-selfsigned.crt" -noprompt
rm -f "$KEYCLOAK_STORE_PATH/keycloak-keystore.p12" 
keytool -import -storetype PKCS12 -keystore "$KEYCLOAK_STORE_PATH/keycloak-keystore.p12" -file "$NGINX_CERT_PATH/nginx-selfsigned.crt" -alias minikube -storepass changeit -noprompt

cd "$SCRIPT_DIR/docker"
docker-compose down
docker-compose up --build reverseproxy --build mockpass -d

cd "$SCRIPT_DIR"
[[ -x "$SCRIPT_DIR/pre-deploy-exec.bash" ]] || chmod +x pre-deploy-exec.bash
skaffold dev
