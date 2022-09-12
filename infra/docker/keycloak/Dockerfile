FROM quay.io/keycloak/keycloak:latest

COPY realms.json "/opt/keycloak/conf/realms.json"
COPY keycloak-broker.p12 "/opt/keycloak/conf/keycloak-truststore.p12"
COPY keycloak-broker.p12 "/opt/keycloak/conf/keycloak-keystore.p12"

ENV JAVA_OPTS_APPEND="-Dkeycloak.import=/opt/keycloak/conf/realms.json"
ENV KC_SPI_TRUSTSTORE_FILE_FILE="/opt/keycloak/conf/keycloak-truststore.p12"
ENV KC_SPI_TRUSTSTORE_FILE_PASSWORD="password"
