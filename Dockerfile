FROM python:3

WORKDIR /usr/src/app

COPY red_team/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install graphviz -y

COPY red_team .
COPY kube-infra ./iac

CMD [ "python", "./main.py" ]
