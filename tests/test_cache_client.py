from gh_user_public_gists_scraper import caching_utils
import pytest

def _redis_up() -> bool:
    import os
    import socket
    try:
        host = os.getenv("CACHE_HOST")
        port = int(os.getenv("CACHE_PORT", "6379"))
        timeout = 30
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

@pytest.fixture
def redis_must_be_down():
    if _redis_up():
        pytest.skip("Redis is up; skipping negative connectivity tests")

def test_cache_client_caching_reqd_False():
    cache = caching_utils.cache_client(caching_required=False)
    assert cache is None

def test_cache_client_caching_reqd_True_no_cache_host():
    import os
    os.environ["CACHE_HOST"] = ""
    with pytest.raises(Exception):
        cache = caching_utils.cache_client(caching_required=True)

def test_cache_client_caching_reqd_True_cache_host_down(redis_must_be_down):
    import os
    import redis
    os.environ["CACHE_HOST"] = "localhost"
    os.environ["CACHE_PORT"] = "6379"
    with pytest.raises(redis.ConnectionError):
        caching_utils.cache_client(caching_required=True)


# This test expects Redis to be down
def test_cache_client_caching_reqd_True_cache_bad_port(redis_must_be_down):
    import os
    os.environ["CACHE_HOST"] = "localhost"
    os.environ["CACHE_PORT"] = "bad_port"
    with pytest.raises(Exception):
        cache = caching_utils.cache_client(caching_required=True)

# This test expects Redis to be down
def test_cache_client_caching_reqd_True_cache_unreachable(redis_must_be_down):
    import os
    import redis
    os.environ["CACHE_HOST"] = "localhost"
    os.environ["CACHE_PORT"] = "6379"
    with pytest.raises(redis.ConnectionError):
        caching_utils.cache_client(caching_required=True)
