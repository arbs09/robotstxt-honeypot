FROM python:3.9-slim AS app

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

ARG ABUSEIPDB_API_KEY
ENV ABUSEIPDB_API_KEY=${ABUSEIPDB_API_KEY}

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
