FROM nginx:alpine
 
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key

#RUN apk update && apk add bash openssl
#RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=*" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
