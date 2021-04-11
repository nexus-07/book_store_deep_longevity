FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN mkdir /django_project
WORKDIR /django_project

COPY . /django_project/
COPY requirements.txt /django_project/

RUN pip install --no-cache-dir -r requirements.txt

ADD . /django_project