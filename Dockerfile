# syntax=docker/dockerfile:1
FROM python:3.10.13
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD ("python","manage.py","runserver")
COPY . /code/
