# query_resolver.py

def resolve_getUserProfile(_, info, id):
    # Placeholder implementation
    return {"id": id, "name": "John Doe", "gender": "Male", "age": 30, "location": "Unknown"}

def resolve_getMatchingResources(_, info, userId):
    return []

from .resource_resolver import resources
def resolve_getAvailableResources(_, info):
    return resources

def resolve_getInclusivityIndex(_, info):
    return {"score": 0.0, "genderEquity": 0.0, "accessToLegalAid": 0.0}

def resolve_getResourceMap(_, info, location):
    return []

def resolve_getReports(_, info):
    return []

def resolve_getUSSDMenu(_, info):
    return []

