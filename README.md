# EmpowerLink Nexus 🛠️🌍

EmpowerLink Nexus is a modular, scalable backend platform designed to address social inclusion, accessibility, and resource distribution challenges through AI-driven services, geospatial mapping, feedback reporting, and telephony integrations. The system is built as a collection of independent microservices communicating via GraphQL APIs and REST, orchestrated through Kubernetes and containerized with Docker.

---

## 📦 Microservices Overview

| Service                       | Description                                                | Tech Stack                                 |
|:-----------------------------|:-----------------------------------------------------------|:-------------------------------------------|
| **[API Gateway](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/api-gateway)**               | Central GraphQL gateway aggregating queries across services | FastAPI, Ariadne, Docker, Kubernetes       |
| **[User Profile Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/user-profile-service)**     | Manages user profiles and authentication                     | FastAPI, Ariadne, SQLAlchemy, PostgreSQL   |
| **[Resource Matching Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/resource-matching-service)** | AI-powered resource matching for users and NGOs               | FastAPI, Scikit-learn, Ariadne, PostgreSQL |
| **[Inclusivity Index Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/inclusivity-index-service)** | Generates inclusivity and accessibility scores for regions    | FastAPI, Celery, Ariadne, PostgreSQL       |
| **[Geospatial Mapping Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/geospatial-mapping-service)** | Maps locations and services with geospatial data               | FastAPI, PostGIS, Ariadne, Docker          |
| **[Reporting & Feedback Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/reporting-feedback-service)** | Collects and manages user feedback and incident reports        | FastAPI, Ariadne, PostgreSQL               |
| **[Telephony Integration Service](https://github.com/MissTipo/EmpowerLink-Nexus/tree/main/services/telephony-integration-service)** | USSD & IVR interfaces for accessibility via basic mobile phones | FastAPI, Ariadne, Docker                   |

---

## 🚀 Technologies Used

- **FastAPI** — for building performant async microservices
- **Ariadne** — lightweight Python GraphQL implementation
- **PostgreSQL/PostGIS** — relational and spatial database support
- **Docker** — containerization for local and production environments
- **Kubernetes (GKE)** — container orchestration and deployment
- **Scikit-learn** — for AI-driven resource matching
- **Celery + Redis** — for background job processing
- **USSD/IVR Integrations** — for mobile telephony access
- **GraphQL Federation** — schema stitching at the API gateway
- **GitHub Actions** — CI/CD pipelines

---

## 📂 Project Structure
```plaintext
empowerlink-nexus/
├── api-gateway/
│   ├── src/
│   │   ├── app.py                   # Main entry point for the GraphQL server
│   │   ├── schema/                  # Consolidated GraphQL schema definitions
│   │   │   ├── index.graphql        # Root schema (imports/subschemas)
│   │   │   ├── user.graphql         # User Profile schema
│   │   │   ├── resource.graphql     # Resource Matching schema
│   │   │   ├── inclusivity.graphql  # Inclusivity Index schema
│   │   │   ├── geospatial.graphql   # Geospatial Mapping schema
│   │   │   ├── feedback.graphql     # Reporting & Feedback schema
│   │   │   └── telephony.graphql    # Telephony Integration schema
│   │   └── resolvers/               # GraphQL resolvers for each service
│   │       ├── user_resolver.py
│   │       ├── resource_resolver.py
│   │       ├── inclusivity_resolver.py
│   │       ├── geospatial_resolver.py
│   │       ├── feedback_resolver.py
│   │       └── telephony_resolver.py
│   ├── config/
│   │   ├── settings.py              # API gateway configuration
│   │   └── logging.yaml             # Logging configuration
│   ├── tests/                       # Unit/integration tests for the gateway
│   ├── Dockerfile                   # Containerization instructions
│   ├── requirements.txt             # Dependencies (e.g., FastAPI, Apollo Server, etc.)
│   └── README.md
├── user-profile-service/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point for user profiles
│   │   ├── models.py                # ORM models (e.g., SQLAlchemy)
│   │   ├── schemas.py               # Pydantic models for validation
│   │   ├── routes.py                # REST endpoints (if needed)
│   │   └── graphql/
│   │       ├── schema.graphql       # GraphQL schema for user profiles
│   │       └── resolvers.py         # GraphQL resolvers for user queries/mutations
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── resource-matching-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── ai/
│   │   │   └── matching_model.py    # Scikit-learn integration for AI matching
│   │   ├── routes.py
│   │   └── graphql/
│   │       ├── schema.graphql
│   │       └── resolvers.py
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── inclusivity-index-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── graphql/
│   │       ├── schema.graphql
│   │       └── resolvers.py
│   ├── workers/
│   │   └── tasks.py                 # Celery tasks for background processing
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── geospatial-mapping-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py                # Models for geospatial data (e.g., PostGIS integration)
│   │   ├── routes.py
│   │   └── graphql/
│   │       ├── schema.graphql
│   │       └── resolvers.py
│   ├── static/                      # Static assets (e.g., Leaflet.js maps, if applicable)
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── reporting-feedback-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── graphql/
│   │       ├── schema.graphql
│   │       └── resolvers.py
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── telephony-integration-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── ussd_routes.py           # Endpoints for USSD interactions
│   │   ├── ivr_routes.py            # Endpoints for IVR interactions
│   │   └── graphql/
│   │       ├── schema.graphql
│   │       └── resolvers.py
│   ├── config/
│   │   └── settings.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── common/                          # Shared libraries/utilities across services
│   ├── utils/
│   │   ├── logger.py                # Common logging utilities
│   │   └── helpers.py               # Helper functions (e.g., formatters, converters)
│   ├── configs/
│   │   └── common_settings.py       # Shared configuration items
│   └── README.md
├── docker-compose.yml               # For local development orchestration
├── k8s/                             # Kubernetes manifests for production deployment
│   ├── api-gateway-deployment.yaml
│   ├── user-profile-deployment.yaml
│   ├── resource-matching-deployment.yaml
│   ├── inclusivity-index-deployment.yaml
│   ├── geospatial-mapping-deployment.yaml
│   ├── reporting-feedback-deployment.yaml
│   ├── telephony-integration-deployment.yaml
│   └── README.md
└── README.md                        # Project overview, setup instructions, etc.

```

