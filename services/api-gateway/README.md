# EmpowerLink Nexus - API Gateway

The API Gateway is the central GraphQL entry point for the EmpowerLink Nexus project. It consolidates multiple microservices—such as User Profile, Resource Matching, Inclusivity Index, Geospatial Mapping, Reporting & Feedback, and Telephony Integration—into a unified GraphQL API. This gateway leverages FastAPI and Ariadne to deliver a schema-first approach for efficient query resolution and modular development.

## Features

- **Unified GraphQL Endpoint:** Combines schemas from multiple microservices into a single API.
- **Schema-First Approach:** Uses `.graphql` files for clear and modular schema definitions.
- **Resolver Mapping:** Connects GraphQL queries and mutations to underlying Python resolver functions.
- **FastAPI Integration:** Provides a robust, asynchronous framework with automatic interactive API docs.
- **Real-Time Updates:** Easily extendable to support real-time data flows with additional tooling (e.g., WebSockets).

## Directory Structure

```plaintext
api-gateway/
├── src/
│   ├── app.py               # FastAPI application entry point; mounts GraphQL endpoint.
│   ├── schema/              # GraphQL schema files (SDL) for all microservices.
│   │   ├── index.graphql
│   │   ├── user.graphql
│   │   ├── resource.graphql
│   │   ├── inclusivity.graphql
│   │   ├── geospatial.graphql
│   │   ├── feedback.graphql
│   │   └── telephony.graphql
│   └── resolvers/           # Python resolver modules for each domain.
│       ├── __init__.py      # (Ensure this file exists to mark the package.)
│       ├── query_resolver.py
│       ├── feedback_resolver.py
│       ├── inclusivity_resolver.py
│       ├── resource_resolver.py
│       ├── geospatial_resolver.py
│       └── telephony_resolver.py
└── README.md                # This file.
```
## Setup & Installation
### Prerequisites

    Python 3.8+
    pip
    Virtual environment tool (optional but recommended)

### Installation Steps

__Clone the repository:__
```bash
git clone <repository-url>
cd EmpowerLink-Nexus/services/api-gateway
```

__Create and activate a virtual environment (optional):__
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

__Install the required packages:__
```bash
    pip install -r requirements.txt
```

        Note: The requirements.txt file is generated from requirements.in and includes all necessary dependencies such as FastAPI, Ariadne, and supporting libraries.

### Running the API Gateway

__Start the FastAPI server using Uvicorn:__
```bash
uvicorn src.app:app --reload
```

The API Gateway will be available at http://localhost:8000/graphql, where you can interact with the GraphQL playground.

## GraphQL Schema & Resolvers

    Schema Files: Located in src/schema/, these files define types, queries, and mutations using the GraphQL SDL.
    Resolvers: Located in src/resolvers/, these Python modules provide the resolver functions for handling GraphQL operations.

This structure enables a clear separation of concerns, making it easier to update or extend the API as the project grows.

## Contributing

__Contributions are welcome! Please follow these steps:__

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Make your changes and commit with clear messages.
    Open a pull request for review.

## License

This project is open-source and available under an OSI-approved license (e.g., MIT, GPL). See the LICENSE file for more details.
Contact

For questions or feedback, please contact the project maintainers or open an issue in the repository.
