#!/bin/bash
set -e
set -o xtrace

[ -n "$GITEA_CLIENT_ID" ] || echo "Set the environment variable GITEA_CLIENT_ID as generated when creating your Gitea OAuth Application."
[ -n "$GITEA_CLIENT_SECRET" ] || echo "Set the environment variable GITEA_CLIENT_SECRET as generated when creating your Gitea OAuth Application."
: ${GITEA_CLIENT_ID:=INVALID_CLIENT_ID}
: ${GITEA_CLIENT_SECRET:=INVALID_CLIENT_SECRET}

sleep 2

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

KEYCLOAK_REALM_PATH="$SCRIPT_DIR/docker/keycloak/realms.json"
KEYCLOAK_REALM_TEMPLATE_PATH="$SCRIPT_DIR/docker/keycloak/realms.json.template"
cat "$KEYCLOAK_REALM_TEMPLATE_PATH" | sed "s/GITEA_CLIENT_ID/$GITEA_CLIENT_ID/g" | sed "s/GITEA_CLIENT_SECRET/$GITEA_CLIENT_SECRETS/g" > "$KEYCLOAK_REALM_PATH"

MINIKUBE_IS_SET_UP="$(minikube profile | grep dev || true)"
KICS_DOCKER_IMAGE_IS_PULLED="$(docker images -q checkmarx/kics)"
[[ -n "$KICS_DOCKER_IMAGE_IS_PULLED" ]] || docker pull checkmarx/kics:latest
[[ -n "$MINIKUBE_IS_SET_UP" ]] || ( minikube start --profile dev && minikube profile dev && minikube addons enable ingress && skaffold config set --global local-cluster true )

KEYCLOAK_STORE_PATH="$SCRIPT_DIR/docker/keycloak/stores"
NGINX_CERT_PATH="$SCRIPT_DIR/docker/reverseproxy/certs"

until [ -n $(minikube ip) ]
do
  echo "Waiting for minikube ingress ip to be up.."
  sleep 2
done

mkdir -p "$NGINX_CERT_PATH"
openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=*" -addext "subjectAltName=DNS:localhost,IP:192.168.49.1" -newkey rsa:2048 -keyout "$NGINX_CERT_PATH/nginx-selfsigned.key" -out "$NGINX_CERT_PATH/nginx-selfsigned.crt"

mkdir -p $KEYCLOAK_STORE_PATH
rm -f "$KEYCLOAK_STORE_PATH/keycloak-truststore.p12" 
keytool -importcert -storetype PKCS12 -keystore "$KEYCLOAK_STORE_PATH/keycloak-truststore.p12" -storepass changeit -alias minikube -file "$NGINX_CERT_PATH/nginx-selfsigned.crt" -noprompt
rm -f "$KEYCLOAK_STORE_PATH/keycloak-keystore.p12" 
keytool -import -storetype PKCS12 -keystore "$KEYCLOAK_STORE_PATH/keycloak-keystore.p12" -file "$NGINX_CERT_PATH/nginx-selfsigned.crt" -alias minikube -storepass changeit -noprompt

cd "$SCRIPT_DIR/docker"
docker-compose down
docker-compose up --build reverseproxy  -d

[[ -x "$SCRIPT_DIR/pre-deploy-exec.bash" ]] || chmod +x pre-deploy-exec.bash

cd "$SCRIPT_DIR"
skaffold dev
