# Geospatial Mapping Service

Provides REST and GraphQL endpoints for spatial resource data and service-desert analysis.

## Features

- **REST**  
  - `GET /map/resources` → GeoJSON FeatureCollection of all resources  
  - `GET /map/service-deserts?radius_km=...` → GeoJSON FeatureCollection of empty grid cells  

- **GraphQL** (POST `/graphql`)  
  - `allResourceLocations: JSON!` → GeoJSON FeatureCollection  
  - `serviceDeserts(radiusKm: Float!): JSON!` → GeoJSON FeatureCollection  

## Getting Started

1. Copy `.env.example` → `.env`:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/geodb
   CORS_ALLOWED_ORIGINS=*

2. Ensure PostGIS is enabled on your DB:
```bash
   psql -h host -U user -d geodb
   \c geodb
   CREATE EXTENSION IF NOT EXISTS postgis;
   
```
3. Build & run:

```bash
   docker build -t geospatial-mapping-service .
   docker run -e DATABASE_URL -p 8000:8000 geospatial-mapping-service
```
4. Test:
```bash
   python3 -m pytest
```

