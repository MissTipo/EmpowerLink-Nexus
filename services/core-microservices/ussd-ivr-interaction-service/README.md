# USSD/IVR Interaction Service

This microservice is part of the EmpowerLink Nexus platform. It handles USSD menu requests and IVR interactions for users with basic mobile phones. The service:
- Receives USSD requests via Kannel.
- Manages USSD session flows using Redis.
- Handles IVR interactions through an Asterisk AGI script.
- Interfaces with the API Gateway by triggering GraphQL mutations.

## Technologies
- **FastAPI** with Strawberry GraphQL
- **Redis** for session management
- **PostgreSQL** (for persistent data, not shown in these examples)
- **Kannel** (USSD gateway) and **Asterisk** (IVR system)
- **Docker** and **Kubernetes** for deployment

## Setup Instructions
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Set up and run Redis and PostgreSQL.
3. Update configuration files in `config/`.
4. Run the service:
    ```bash
    uvicorn main:app --reload
    ```
5. For IVR testing, ensure Asterisk is installed and configured.

## Testing
Run tests using pytest:
```bash
pytest tests/

