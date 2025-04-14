# tests/test_auth.py

import pytest

def execute_graphql_query(client, query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = client.post("/graphql", json=payload)
    assert response.status_code == 200, f"Status: {response.status_code}, {response.text}"
    return response.json()["data"]

def test_signup_and_signin(client):
    # Test GraphQL mutation to sign up an organization
    signup_mutation = """
    mutation SignupOrganization($input: OrganizationInput!) {
      signupOrganization(input: $input) {
        id
        name
        email
      }
    }
    """
    signup_variables = {
        "input": {
            "name": "EmpowerOrg",
            "email": "contact@empowerorg.com",
            "phone": "0712345678",
            "location": "Nairobi",
            "role": "Organization",
            "password": "password123"
        }
    }
    signup_data = execute_graphql_query(client, signup_mutation, signup_variables)
    org = signup_data.get("signupOrganization")
    assert org is not None, "Signup failed, returned None"
    assert org["email"] == "contact@empowerorg.com", f"Unexpected email: {org.get('email')}"

    # Test GraphQL mutation for sign-in
    signin_mutation = """
    mutation SigninOrganization($email: String!, $password: String!) {
      signinOrganization(email: $email, password: $password) {
        access_token
        token_type
      }
    }
    """
    signin_variables = {
        "email": "contact@empowerorg.com",
        "password": "password123"
    }
    signin_data = execute_graphql_query(client, signin_mutation, signin_variables)
    token = signin_data.get("signinOrganization")
    assert token is not None, "Signin failed, token is None"
    assert token["token_type"] == "bearer", f"Unexpected token type: {token.get('token_type')}"

