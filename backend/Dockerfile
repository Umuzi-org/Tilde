FROM python:3.7 

# based on https://docs.docker.com/compose/django/https://docs.docker.com/compose/django/+
RUN pip install --upgrade pip
RUN pip install gunicorn

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000

CMD gunicorn -b :8080 --log-level debug backend.wsgi

