#!/usr/bin/env python3
import sys
import json
import requests

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    mode = sys.argv[1]

    # GraphQL endpoint (update as necessary)
    graphql_endpoint = "http://api.yourdomain.com/graphql"
    headers = {"Content-Type": "application/json"}

    if mode == "report":
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
                "type": "incident",
                "details": "IVR report triggered",
                "sender": "IVR_USER"
            }
        }
    elif mode == "support":
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
                "type": "support",
                "details": "IVR support request triggered",
                "sender": "IVR_USER"
            }
        }
    else:
        sys.exit(1)

    payload = {"query": mutation, "variables": variables}
    try:
        response = requests.post(graphql_endpoint, headers=headers, json=payload)
        print("GraphQL response:", response.json())
    except Exception as e:
        print("Error sending GraphQL mutation:", e)

if __name__ == "__main__":
    main()

