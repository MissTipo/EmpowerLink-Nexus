FROM python:3.10-slim

# install PostGIS client dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gdal-bin libproj-dev postgresql-client-15 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY config/ ./config/
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

