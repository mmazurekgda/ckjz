import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ckjz import __version__
from ckjz.api import router as api_router
from ckjz.frontend import ui


app = FastAPI(
    title="CKJZ",
    description="A simple API for the CKJZ project.",
    version=__version__,
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


app.include_router(api_router)

static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

ui.run_with(
    app,
    mount_path='/',
    storage_secret='pick your private secret here',
    tailwind=True,
    title="CKJZ",
)

