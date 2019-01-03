FROM python:3.6.5

WORKDIR /opt/crawler

COPY apt-pkgs.txt ./
RUN apt-get update && apt-get install -q -y $(cat apt-pkgs.txt)

COPY requirements.txt ./
RUN pip install -r requirements.txt -v

ENV BROKER_URL="amqp://guest:guest@rabbitmq:5672//" \
    BACKEND_URL="redis://redis:6379/0"

COPY src ./
CMD celery worker -A worker -E -l info
