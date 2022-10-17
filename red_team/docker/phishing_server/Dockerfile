FROM golang:latest

WORKDIR /usr/src/app

RUN wget https://github.com/imthaghost/goclone/releases/download/v1.2.0/goclone_1.2.0_Linux-64bit.tar.gz
RUN tar -xzvf goclone_1.2.0_Linux-64bit.tar.gz
RUN apt update && apt install jq xdg-utils -y

COPY . .

RUN echo "./goclone --serve \"$(cat .out/sso.json | jq -r .idp.authorizationUrl)?response_type=code&client_id=$(cat .out/sso.json | jq -r .idp.clientId)&redirect_uri=http%3A%2F%2F$(cat .out/sso.json | jq -r .idp.domain)%2Fauth%2Frealms%2F$(cat .out/sso.json | jq -r .authenticator.realm)%2Fbroker%2Foidc%2Fendpoint\"" > run.bash

CMD [ "bash", "run.bash" ]
