# feedback_resolver.py

def resolve_submitReport(_, info, input):
    return {
        "id": "1",
        "userId": input["userId"],
        "type": input["type"],
        "description": input["description"],
        "createdAt": "2025-03-21T00:00:00Z"
    }

def resolve_submitFeedback(_, info, input):
    return {
        "id": "1",
        "userId": input["userId"],
        "feedback": input["feedback"],
        "createdAt": "2025-03-21T00:00:00Z"
    }

