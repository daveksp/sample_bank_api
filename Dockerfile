FROM python:3.8-slim

RUN apt-get -y update && apt-get install -y libzbar-dev python-mysqldb default-libmysqlclient-dev

ADD . /code
WORKDIR /code

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8089
#ENV FLASK_APP=manage.py
#FLASK_ENV=development
CMD python manage.py run --host 0.0.0.0 -p 8089
