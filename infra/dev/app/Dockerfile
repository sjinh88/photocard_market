FROM python:3.10.6
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /photocard_market
RUN mkdir /photocard_market/infra

COPY requirements.txt /photocard_market/
RUN pip install -r requirements.txt
RUN pip install mysqlclient
COPY infra/dev/uwsgi/uwsgi.ini /

# Copy the Django project
COPY ../../photocard_market /photocard_market/

EXPOSE 8000
