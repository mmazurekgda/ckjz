from fastapi import FastAPI

from ckjz import __version__
from ckjz.api import router as api_router

app = FastAPI(
    title="CKJZ",
    description="A simple API for the CKJZ project.",
    version=__version__,
)

app.include_router(api_router)



# @app.get("/healthz/{toilet_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}