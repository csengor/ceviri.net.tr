FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY . /app/

RUN apt-get update && apt-get install -y gettext postgresql-client
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
