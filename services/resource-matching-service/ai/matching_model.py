import os
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from config.settings import settings

# Load transformer and model at startup
with open(settings.transformer_path, 'rb') as f:
    transformer: ColumnTransformer = pickle.load(f)
with open(settings.model_path, 'rb') as f:
    nn: NearestNeighbors = pickle.load(f)

# Correctly load resource_ids.pkl from the ai directory
current_dir = os.path.dirname(__file__)
resource_ids_path = os.path.join(current_dir, "resource_ids.pkl")
with open(resource_ids_path, 'rb') as f:
    resource_ids = pickle.load(f)

def match_resources(request_dict: dict, limit: int):
    df = pd.DataFrame([{
        'service_type': request_dict['service_type'],
        'latitude': request_dict['location']['latitude'],
        'longitude': request_dict['location']['longitude'],
        'cost_level': request_dict.get('cost_level', 0)
    }])
    X_user = transformer.transform(df)
    distances, indices = nn.kneighbors(X_user, n_neighbors=limit)
    return [
        {'resource_id': resource_ids[i], 'distance': float(distances[0][idx])}
        for idx, i in enumerate(indices[0])
    ]

