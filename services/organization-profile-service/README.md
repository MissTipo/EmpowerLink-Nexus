# Organization Auth Service

The Organization Auth Service is a microservice designed to handle the authentication and profile management for organizations, NGOs, policy makers, and other authorized users accessing the EmpowerLink Nexus dashboard. It exposes a GraphQL API (using Ariadne) and optional REST endpoints, and uses PostgreSQL as its database. The service provides secure registration, sign-in, and token verification using OAuth2 with JWT.

## Features

- **User Registration:**  
  Organizations can register by providing essential details such as name, email, password, and role.

- **User Login:**  
  Registered organizations can log in with email and password. Successful authentication returns a JWT token for accessing secured routes.

- **Token Verification:**  
  Validate and decode JWT tokens to ensure secure, role-based access to the dashboard.

- **GraphQL API:**  
  Exposes queries and mutations to register, log in, and manage organization profiles.
  
- **Optional REST Endpoints:**  
  Provides additional RESTful routes for organization management.

## Technology Stack

- **Backend:** FastAPI
- **GraphQL:** Ariadne
- **Database:** PostgreSQL (via SQLAlchemy)
- **Authentication:** JWT (using jose)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Environment Configuration:** `.env` file with Pydantic BaseSettings

## Directory Structure
```plaintext

organization-auth-service/
├── app/
│   ├── auth/
│   │   ├── jwt.py           # JWT token generation/validation functions
│   │   └── security.py      # Authentication dependencies (OAuth2)
│   ├── graphql/
│   │   ├── resolvers.py     # GraphQL resolver functions
│   │   └── schema.graphql   # GraphQL schema definitions (SDL)
│   ├── models.py            # SQLAlchemy models for organizations
│   ├── database.py          # Database connection and dependency (SQLAlchemy)
│   ├── schemas.py           # Pydantic schemas for input and output
│   ├── routes.py            # REST API endpoints for organization auth
│   └── main.py              # FastAPI app entry point
├── tests/
│   └── test_auth.py         # Tests for authentication and core operations
├── Dockerfile               # Dockerfile for containerizing the service
├── docker-compose.yml       # (optional) Docker Compose configuration for local development
├── .env                     # Environment variables (DATABASE_URL, SECRET_KEY, etc.)
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (or use Docker to run a PostgreSQL container)
- Docker (for containerization)
- Git (for source control)

### Environment Setup

1. Create a `.env` file in the root of the service with the following variables:

   ```env
   DATABASE_URL=postgresql://org_user:org_pass@localhost/organization_db
   SECRET_KEY=your-super-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
Adjust the DATABASE_URL parameters (username, password, host, and database name) according to your PostgreSQL setup.
Running Locally

2. Install Dependencies:
  
  ```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Set Up the Database:

Ensure your PostgreSQL database is running and accessible via the URL provided in your .env file. For local development, you can use Docker:
```bash
docker compose up -d
```

(If you have a Docker Compose file set up for PostgreSQL, see the project README.)

4. Run the Service:
```bash

    uvicorn app.main:app --reload --port 8002
```

    The service will be available at http://localhost:8002 and the GraphQL playground at http://localhost:8002/graphql.

## Docker

To build the Docker image:
```bash

docker build -t misstipo/organization-auth-service:latest .
```

To run the container locally:
```bash

docker run -p 8002:8002 misstipo/organization-auth-service:latest
```

## CI/CD

This service is integrated into your CI/CD pipeline using GitHub Actions. The pipeline runs tests, builds and pushes the Docker image, and deploys the service to your Kubernetes cluster using GKE.
API Endpoints
GraphQL

Access the GraphQL Playground at:

http://localhost:8002/graphql

**GraphQL Schema includes:**

    Queries:

        getOrganizationByEmail(email: String!): Organization

        verifyOrganizationToken(token: String!): TokenInfo

    Mutations:

        registerOrganization(input: OrganizationInput!): Organization

        loginOrganization(input: LoginInput!): AuthPayload

## REST (Optional)

Endpoints for managing organization profiles:

    POST /api/org/organizations/: Create a new organization.

    POST /api/org/auth/login: Log in and get JWT token.

## Authentication

    JWT Authentication:
    After logging in, organizations receive an access token.
    Use the token in the Authorization header as Bearer <token> to access secured endpoints or GraphQL queries.

## Testing

Run tests with:
```bash

python3 -m pytest
```

Tests are located in the tests/ directory.

## Contributing

Contributions to this service are welcome! Please follow the repository guidelines and open issues or pull requests for improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
