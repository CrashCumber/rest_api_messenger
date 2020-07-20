FROM python:3.6

COPY ./app /app
COPY ./requirements.txt /
COPY ./config.py /
COPY ./manage.py /
COPY ./wait-for-it.sh /
RUN pip install -r /requirements.txt

RUN chmod +x manage.py
RUN chmod 777 wait-for-it.sh

RUN python manage.py db init

EXPOSE 5000


