import requests
import json

def trigger_graphql_mutation(action: str, details: str, sender: str, graphql_endpoint: str):
    headers = {"Content-Type": "application/json"}
    mutation = """
    mutation CreateReport($input: ReportInput!) {
        createReport(input: $input) {
            id
            status
        }
    }
    """
    variables = {
        "input": {
            "type": action,
            "details": details,
            "sender": sender
        }
    }
    payload = {"query": mutation, "variables": variables}
    try:
        response = requests.post(graphql_endpoint, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print("GraphQL mutation error:", e)
        return None

