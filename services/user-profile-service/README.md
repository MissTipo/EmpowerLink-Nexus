# User Profile Service

This service manages user profiles for EmpowerLink Nexus. It provides both REST endpoints and a GraphQL API to create, retrieve, and update user profiles.

## Features

- **User Profile Management:**  
  Create, read, and update user profiles.
- **GraphQL API:**  
  Exposes a GraphQL endpoint (`/graphql`) with the following operations:
  - `getUserProfile(id: ID!): UserProfile`
  - `createUserProfile(input: UserProfileInput!): UserProfile`
  - `updateUserProfile(id: ID!, input: UserProfileInput!): UserProfile`
- **REST Endpoints:**  
  Optionally available under `/api/users` for integration or administrative purposes.
- **Database:**  
  Uses SQLAlchemy as the ORM. Currently configured for SQLite for quick development; production should use PostgreSQL or another robust database.

## Setup and Installation

### Requirements

- Python 3.10+
- [pip](https://pip.pypa.io)

### Installation

1. Clone the repository and navigate to the `user-profile-service` directory.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    ```bash
    alembic upgrade head
    ```
5. Run the application:
    ```bash
    uvicorn app.main:app --reload --port 8001
    ```

## Docker
To build and run the Docker container:
```bash
docker build -t user-profile-service .
docker run -p 8001:8001 user-profile-service
```
## Testing
Run the tests with:
```bash
pytest --maxfail=1 --disable-warnings -q
```

## API Endpoints
- **REST API:**
    - GET /api/users/{user_id}: Retrieves a user profile.
    - POST /api/users/: Creates a new user profile.
    - PUT /api/users/{user_id}: Updates an existing user profile.

- **GraphQL API:**
    - Accessible at /graphql.

## Configuration

Database configuration and other settings are located in config/settings.py.

## License

This project is open-source under the MIT License.
