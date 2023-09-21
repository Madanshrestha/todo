FROM python:3.12.0rc2-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

WORKDIR /todo

COPY requirements.txt /todo/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /todo/
