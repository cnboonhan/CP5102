FROM python:3

WORKDIR /usr/src/app

COPY proxy.requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update

COPY . .

CMD [ "python", "proxy_server.py"]
