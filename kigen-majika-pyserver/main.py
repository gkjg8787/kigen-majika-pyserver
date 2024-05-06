from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from router import api, items

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.router)
app.include_router(items.router)


@app.get("/")
async def root(request: Request):
    return RedirectResponse(
        url=request.url_for("read_users_items"), status_code=status.HTTP_302_FOUND
    )
