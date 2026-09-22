from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import status

app = FastAPI()

@app.get("/{USER}")
def get_user_gists(USER: str):
    return JSONResponse(status_code=status.HTTP_200_OK)

@app.get("/")
def docs():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
