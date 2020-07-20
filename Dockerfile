FROM python:3.6

COPY ./app /app
COPY ./requirements.txt /
COPY ./config.py /
COPY ./manage.py /
RUN pip install -r /requirements.txt

RUN chmod +x manage.py

RUN python manage.py db init

EXPOSE 5000


