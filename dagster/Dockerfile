FROM python:3.11-slim

ENV PYTHONPATH=/app
ENV DAGSTER_HOME=/opt/dagster/dagster_home

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/dagster/dagster_home

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-w", "workspace.yaml"]