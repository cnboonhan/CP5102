FROM quay.io/keycloak/keycloak:latest

COPY realms.json /opt/jboss/keycloak/realms.json
COPY stores/keycloak-truststore.p12 /usr/src/stores/keycloak-truststore.p12

ENV JAVA_OPTS_APPEND="-Dkeycloak.import=/opt/jboss/keycloak/realms.json"
ENV KC_SPI_TRUSTSTORE_FILE_FILE="/usr/src/stores/keycloak-truststore.p12"
ENV KC_SPI_TRUSTSTORE_FILE_PASSWORD="changeit"
