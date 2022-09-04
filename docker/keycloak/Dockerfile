FROM quay.io/keycloak/keycloak:latest

COPY realms.json /opt/jboss/keycloak/realms.json

ENV JAVA_OPTS_APPEND="-Dkeycloak.import=/opt/jboss/keycloak/realms.json"
