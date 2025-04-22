# Empowerlink Nexus Resource Matching Service

This microservice provides both GraphQL and health endpoints to match users to resources using a K‑Nearest Neighbors model. It is built with FastAPI, Ariadne, SQLAlchemy, and scikit‑learn.

## Setup
1. Create a `.env` file with `DATABASE_URL=postgresql://user:pass@host/dbname`.
2. `pip install -r requirements.txt`
3. Prepare and pickle your transformer, model, and resource_ids into `app/ai/`:
   ```python
   # example: fit & pickle transformer, nn, ids
   import pickle, pandas as pd
   from sklearn.compose import ColumnTransformer
   # ...
