import json
import redis.asyncio as redis

# Configure your Redis connection
redis_client = redis.from_url("redis://localhost:6379/0", decode_responses=True)

async def get_session(sender: str):
    session_key = f"ussd_session:{sender}"
    session = await redis_client.get(session_key)
    if session is None:
        session_data = {"step": 0}
    else:
        session_data = json.loads(session)
    return session_data, session_key

async def update_session(session_key: str, session_data: dict, timeout: int = 300):
    await redis_client.set(session_key, json.dumps(session_data), ex=timeout)

async def clear_session(session_key: str):
    await redis_client.delete(session_key)

