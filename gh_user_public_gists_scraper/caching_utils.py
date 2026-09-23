import redis
import os

def cache_client(caching_required: bool=True) -> redis.Redis | None:
    try:
        if not caching_required:
            return None
        cache_host = os.getenv("CACHE_HOST")
        cache_port = int(os.getenv("CACHE_PORT", "6379"))
        if not (cache_host):
            raise Exception("Will not be able to connect to caching host despite `caching_required` being set to True. Please consider setting the environment variable CACHE_HOST.")
        cache_db = os.getenv("CACHE_DB", "0")
        connection_string_redis = f"redis://{cache_host}:{cache_port}/{cache_db}"
        client = redis.from_url(connection_string_redis)
        if not client.ping():
            raise redis.ConnectionError(f"Unable to connect to the cache host at {cache_host}")
        return client
    except:
        raise
