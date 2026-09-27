import requests
from . import caching_utils
from typing import Any, List


def write_gists_to_cache(cache_key: str, data_to_cache: Any):
    try:
        import json
        cache_client = caching_utils.cache_client(True)
        pipe = cache_client.pipeline()
        pipe.delete(cache_key)
        if data_to_cache:
            pipe.rpush(
                cache_key,
                *[json.dumps(item) for item in data_to_cache],
            )
            pipe.expire(cache_key, 900)
        pipe.execute()
    except:
        raise

def read_gists_from_cache(cache_key: str) -> List[dict]|None:
    try:
        import json
        cache_client = caching_utils.cache_client(True)
        cached_items = cache_client.lrange(cache_key, 0, -1)
        if not cached_items:
            return None
        return [json.loads(item) for item in cached_items]
    except:
        raise

def generate_user_gist_url(user: str, github_api_url: str="https://api.github.com") -> str:
    try:
        if not (user and user.strip()):
            raise ValueError("When generating a user gist URL, the user cannot be an empty string")
        return f"{github_api_url}/users/{user}/gists"
    except (ValueError, ):
        raise


def response_from_github_api(url: str, headers: dict, method: str, **kwargs) -> requests.Response | None:
    try:
        if method not in set[str](["GET", "PUT", "POST", "PATCH", "DELETE", "OPTIONS"]):
            raise ValueError(f"The HTTP method {method} is not known")
        res = requests.request(
            headers=headers,
            url=url,
            method=method,
            **kwargs
        )
        res.raise_for_status()
        return res
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ):
        raise


def get_gist_for_user(
        user: str,
        github_api_key: str|None,
        write_to_cache: bool=True,
        github_api_url: str="https://api.github.com",
        max_pages: int=5
    ) -> List[dict]|None:
    request_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    if github_api_key is not None and (github_api_key.startswith("ghp") or github_api_key.startswith("github_pat")):
        request_headers["Authorization"] = github_api_key
    pages_scrolled = 0
    obtained_gists = []
    try:
        cached_gists = read_gists_from_cache(user)
        if cached_gists:
            return cached_gists
        gists_url = f"{github_api_url}/users/{user}/gists"
        res = response_from_github_api(
            gists_url,
            request_headers,
            "GET",
        )
        for gist in res.json():
            obtained_gists.append(gist)
        # until users with a very large number of gists can be handled efficiently,
        # while also keeping github's "authenticated requests" Rate-limits in mind
        # we will keep only 5 pages worth of gists by default.
        pages_scrolled += 1
        while (res.links is not None and pages_scrolled < max_pages):
            url_next = res.links.get("next")
            if url_next is None:
                break
            res = response_from_github_api(
                url=url_next.get("url"),
                headers=request_headers,
                method="GET"
            )
            for gist in res.json():
                obtained_gists.append(gist)
            pages_scrolled += 1
        if write_to_cache:
            write_gists_to_cache(cache_key=user, data_to_cache=obtained_gists)
        return obtained_gists
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, OSError, Exception):
        if obtained_gists:
            return obtained_gists
        raise
