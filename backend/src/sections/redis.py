from redis import Redis
from src.configs.settings import Config


# jwt id
JTI_EXPIRY = 3600


redis_client = Redis(
    host = Config.REDIS_HOST,
    port = Config.REDIS_PORT,
    db=0
)


async def add_jti_to_blocklist(jti: str) -> None:
    redis_client.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = redis_client.get(jti)
    return jti is not None