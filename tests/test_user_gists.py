from gh_user_public_gists_scraper import gh_gist_scraper
import pytest

def test_generate_user_gist_url_empty_user():
    user = "\
    "
    with pytest.raises(ValueError):
        gh_gist_scraper.generate_user_gist_url(user=user)

def test_generate_user_gist_url_non_empty_user():
    user = "HugsLibRecordKeeper"
    user_gist_url = gh_gist_scraper.generate_user_gist_url(user=user)
    assert user_gist_url is not None
    assert user_gist_url == f"https://api.github.com/users/{user}/gists"


def test_response_from_github_api_unsupported_method():
    user = "HugsLibRecordKeeper"
    user_gist_url = gh_gist_scraper.generate_user_gist_url(user=user)
    request_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    method = "BAD_METHOD"
    with pytest.raises(ValueError):
        gh_gist_scraper.response_from_github_api(
            user_gist_url,
            headers=request_headers,
            method=method
        )


def test_response_from_github_api_bad_method():
    user = "HugsLibRecordKeeper"
    user_gist_url = gh_gist_scraper.generate_user_gist_url(user=user)
    request_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    method = "POST"
    with pytest.raises(ValueError):
        gh_gist_scraper.response_from_github_api(
            user_gist_url,
            headers=request_headers,
            method=method
        )


def test_response_from_github_api_acceptable_method():
    user = "HugsLibRecordKeeper"
    user_gist_url = gh_gist_scraper.generate_user_gist_url(user=user)
    request_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    method = "GET"
    resp = gh_gist_scraper.response_from_github_api(
        user_gist_url,
        headers=request_headers,
        method=method
    )
    assert resp is not None
    assert resp.status_code >= 200 and resp.status_code <= 400


def test_get_gist_for_user_with_authentication_no_cache():
    import os
    github_api_key = os.getenv("GITHUB_API_TOKEN")
    user = "HugsLibRecordKeeper"
    gists_for_user = gh_gist_scraper.get_gist_for_user(
        user=user,
        write_to_cache=False,
        github_api_key=github_api_key
    )
    assert gists_for_user is not None
    assert len(gists_for_user) >= 1


def test_get_gist_for_user_with_authentication_cache():
    import os
    github_api_key = os.getenv("GITHUB_API_TOKEN")
    user = "HugsLibRecordKeeper"
    gists_for_user = gh_gist_scraper.get_gist_for_user(
        user=user,
        write_to_cache=True,
        github_api_key=github_api_key
    )
    assert gists_for_user is not None
    assert len(gists_for_user) >= 1
