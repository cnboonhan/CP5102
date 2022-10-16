FROM python:3

WORKDIR /usr/src/app

COPY red-team/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install graphviz -y

COPY red-team .
COPY kube-infra ./kube-infra

CMD [ "python", "main.py" ]
