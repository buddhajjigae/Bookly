FROM python:3.5-slim

MAINTAINER fernando@linuxacademy.com (modified by dff)

USER root

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "run_app.py"]