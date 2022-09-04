FROM nginx:alpine
 
 COPY nginx.conf /etc/nginx/nginx.conf

RUN apk update && apk add bash openssl

 RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=mockpass.cp5102.edu" -addext "subjectAltName=DNS:mockpass.cp5102.edu" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt;
