FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt
COPY ./templates/index.html /app/templates/index.html
COPY ./app.py /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python3 app.py