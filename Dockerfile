FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY manage.py .
COPY userApi userApi
COPY api api
COPY emailSending emailSending
COPY usrLogin usrLogin

CMD python manage.py runserver 0.0.0.0:8081