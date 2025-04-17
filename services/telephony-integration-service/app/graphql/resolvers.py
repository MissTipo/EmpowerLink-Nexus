# telephony-integration-service/app/graphql/resolvers.py

def resolve_dummy(_, info):
    return "dummy response"

def resolve_dummy_mutation(_, info):
    return "dummy mutation executed"

