# Stage 1: Runtime image
FROM python:3.10-slim AS runtime

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY config/ ./config/
COPY ai/ ./ai/

# Copy the pre-trained model into the expected location
COPY ai/knn_model.pkl ./ai/knn_model.pkl

# Expose the GraphQL port
EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]

