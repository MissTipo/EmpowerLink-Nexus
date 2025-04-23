# Stage 1: Base image for training
FROM python:3.10-slim AS trainer

WORKDIR /workspace

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only what’s needed to install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy AI code and train
COPY config/ ./config/
COPY ai/ ./ai/
RUN python -m ai.matching_model  \
    && mv models/trained_model.pkl artifacts/

# Stage 2: Runtime image
FROM python:3.10-slim AS runtime

WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Copy the trained artifact from the trainer stage
COPY --from=trainer /workspace/artifacts/trained_model.pkl ./app/ai/trained_model.pkl

# Expose the GraphQL port
EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]

