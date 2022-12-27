FROM python:3.7-slim

COPY requirements.txt .
RUN python -m pip install -r requirements.txt


EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
