FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles
COPY ./requirements.txt .
RUN pip install -r requirements.txt