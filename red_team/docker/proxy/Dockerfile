FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r docker/proxy/requirements.txt


COPY lib docker/proxy/lib
CMD [ "python", "docker/proxy/main.py" ]
