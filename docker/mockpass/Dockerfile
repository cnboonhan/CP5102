FROM node:slim

# Depends on setup-all.bash script to copy exported certs from minikube
COPY certs/ /usr/src/certs
ENV SERVICE_PROVIDER_CERT_PATH=/usr/src/certs/ingress-cert.pem
ENV SERVICE_PROVIDER_PUB_KEY=/usr/src/certs/ingress-pubkey.pem
ENV SHOW_LOGIN_PAGE=true

WORKDIR /usr/src/mockpass

RUN npm install @opengovsg/mockpass

CMD ["npx", "mockpass"]
