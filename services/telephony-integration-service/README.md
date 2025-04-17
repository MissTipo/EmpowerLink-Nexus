# Telephony Integration Service

This service simulates USSD and IVR interactions for the EmpowerLink Nexus platform. It is designed to:
- Accept USSD requests on the shortcode *999#.
- Provide a multi-step registration flow for users, including language selection, name, and location input.
- Respond with a service menu after successful registration or if the user is already registered.
- Handle IVR interactions via a simple endpoint.

## USSD Flow Example

1. **User Dials:**  
   *999#

2. **Language Selection:**  
   The user is prompted to select a language (e.g., 1 for English, 2 for Kiswahili).

3. **Registration:**  
   - If not already registered, the user is asked to enter their name (or press 0 to skip).
   - Next, the user is asked to enter their location.
   - The service then calls a GraphQL mutation on the user-profile-service to create their profile.
   - The user is then presented with a service menu:
     ```
     1. Health Assistance
     2. Police & Justice Help
     3. Social Support Services
     ```

4. **IVR Flow:**  
   For IVR, a similar interaction occurs via voice prompts at the number 300 (currently a placeholder).

## Running the Service

- **Local Development:**  
  Run the service using:
  ```bash
  uvicorn app.main:app --reload --port 8002

## Environment Variables:
  Set up a .env file in the root of this service (if needed) with:
```bash
    USER_PROFILE_GRAPHQL_URL=http://user-profile-service:8001/graphql
```

## Containerization

  **Docker:** 
    Build the Docker image using the provided Dockerfile:
```bash
    docker build -t misstipo/telephony-integration-service:latest .
```
## Testing
```bash
  python3 -m pytest
```
