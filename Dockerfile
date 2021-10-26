FROM python:3.9

EXPOSE 8080

RUN mkdir app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG data_path=/app/data

ENV TIMEZONE="Europe/Madrid" LOG_LEVEL="INFO"
# Estas variables deben sustituirse para que funcione la app
ENV FICHAJE=http://example.com

CMD ["uwsgi", "uwsgi.ini"]
COPY wsgi_app.py .

COPY openhrapi ./openhrapi/
COPY uwsgi.ini .
