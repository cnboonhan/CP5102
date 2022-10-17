FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r docker/extract_sso/requirements.txt

COPY lib docker/extract_sso/lib
CMD [ "python", "docker/extract_sso/main.py" ]
