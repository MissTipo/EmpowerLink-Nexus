# resource_resolver.py

def resolve_requestResourceMatching(_, info, userId, resourceId):
    return {"userId": userId, "resourceId": resourceId, "matchedAt": "2025-03-21T00:00:00Z"}


resources = []  # Temporary in-memory storage

def resolve_addResource(_, info, type, description, location):
    new_resource = {
        "id": str(len(resources) + 1),
        "type": type,
        "description": description,
        "location": location,
    }
    resources.append(new_resource)
    return new_resource

