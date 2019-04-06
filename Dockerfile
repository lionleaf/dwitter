FROM nikolaik/python-nodejs:latest

WORKDIR /app

EXPOSE 8000

COPY . /app

RUN make setup

RUN make

CMD python manage.py runserver 0.0.0.0:8000
