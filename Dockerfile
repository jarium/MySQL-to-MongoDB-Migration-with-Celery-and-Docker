FROM python:3.8

EXPOSE 5000

WORKDIR /app

RUN pip install pymongo mysql-connector pandas numpy dnspython celery sqlalchemy PyAMQP




COPY tasks.py /app/