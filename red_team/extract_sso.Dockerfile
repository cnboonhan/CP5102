FROM python:3

WORKDIR /usr/src/app

COPY extract-sso.requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "extract_sso.py" ]
