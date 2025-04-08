# user-profile-service/app/graphql/resolvers.py

# Dummy in-memory storage for demonstration purposes
# Later, you can integrate with the models and actual database logic.
DUMMY_USER = {
    "id": "1",
    "phone_number": "1234567890",
    "name": "John Doe",
    "gender": "Male",
    "age": 30,
    "location": "Unknown",
    "created_at": "2025-01-01T00:00:00Z"
}

def resolve_getUserProfile(_, info, id):
    # Placeholder: always return the dummy user for id "1"
    if id == "1":
        return DUMMY_USER
    return None

def resolve_createUserProfile(_, info, input):
    # Here, you would normally store the new user and return it
    created_user = {"id": "2", **input, "created_at": "2025-01-02T00:00:00Z"}
    return created_user

def resolve_updateUserProfile(_, info, id, input):
    # Placeholder: update the dummy user if id matches
    if id == "1":
        updated_user = {**DUMMY_USER, **input}
        return updated_user
    return None

