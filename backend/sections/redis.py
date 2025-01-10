from typing import Annotated
from fastapi import Depends
from redis import Redis
from redis import asyncio as async_redis
from backend.settings import Config


# jwt id
JTI_EXPIRY = 3600


async def add_jti_to_blocklist(jti: str, redis_client: async_redis.Redis) -> None:
    print("REDIS TASK STARTED (adding token to blocklist)...")
    try:
        await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)
    except Exception as error:
        print("\nERROR Redis add jti\n", error)
    print("REDIS TASK FINISHED.")


# returns true if given exists
# False if it is None
async def token_in_blocklist(jti: str, redis_client: async_redis.Redis) -> bool:
    try:
        jti = await redis_client.get(jti)
    except Exception as error:
        print("\nERROR Redis blocklist\n", error)
    print("REDIS TASK (Token check)")
    return jti is not None


async def get_redis():
    async with async_redis.Redis.from_url(Config.REDIS_URL) as client:
        yield client


getRedisDep = Annotated[Redis, Depends(get_redis)]