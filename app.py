from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import status
from gh_user_public_gists_scraper import gh_gist_scraper
import os

app = FastAPI()

ENABLE_RESPONSE_CACHING = os.getenv("ENABLE_RESPONSE_CACHING")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

@app.get("/{USER}")
def get_user_gists(USER: str):
    try:
        gists_for_user = gh_gist_scraper.get_gist_for_user(
            USER,
            write_to_cache=ENABLE_RESPONSE_CACHING,
            github_api_key=GITHUB_API_KEY
        )
        return JSONResponse(content=gists_for_user)
    except:
        raise

@app.get("/")
def docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
