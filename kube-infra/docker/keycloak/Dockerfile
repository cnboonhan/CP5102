FROM quay.io/keycloak/keycloak:latest

ARG KEYCLOAK_IDP_HOST
ENV KEYCLOAK_IDP_HOST=$KEYCLOAK_IDP_HOST
ARG MINIKUBE_INGRESS_HOST
ENV MINIKUBE_INGRESS_HOST=$MINIKUBE_INGRESS_HOST

#COPY realms.json "/opt/keycloak/conf/realms.json"
COPY truststore.p12 "/opt/keycloak/conf/truststore.p12"

#RUN sed -i "s/auth.cp5102.edu/$KEYCLOAK_IDP_HOST/g" "/opt/keycloak/conf/realms.json"
#RUN sed -i "s/192.168.49.2/$MINIKUBE_INGRESS_HOST/g" "/opt/keycloak/conf/realms.json"

#ENV JAVA_OPTS_APPEND="-Dkeycloak.import=/opt/keycloak/conf/realms.json"
ENV KC_SPI_TRUSTSTORE_FILE_FILE="/opt/keycloak/conf/truststore.p12"
ENV KC_SPI_TRUSTSTORE_FILE_PASSWORD="password"
