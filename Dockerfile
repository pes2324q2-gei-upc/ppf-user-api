FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY manage.py .
COPY users users

CMD python manage.py runserver