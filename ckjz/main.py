import os
import asyncio
import json
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
from starlette.websockets import WebSocketDisconnect
from sqlmodel import Session, select
from ckjz.models.toilet import Toilet
from ckjz.engine import engine
from ckjz.constants import WS_STATUSES, TIME_DELTA_WATCHDOG, TIME_DELTA_UPDATES
from ckjz import __version__
from ckjz.api import router as api_router
from ckjz.frontend import ui
from ckjz.manager import manager


app = FastAPI(
    title="CKJZ",
    description="A simple API for the CKJZ project.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.receive_text()
        await monitor_status(websocket)
    #await manager.connect(websocket)
    #try:
    #    while True:
    #        print(f"Connections: {len(manager.active_connections)}")
    #        await monitor_status(websocket)
    #        await asyncio.sleep(TIME_DELTA_UPDATES)
    #except WebSocketDisconnect:
    #    print("Closing connection")
    #    await websocket.close()


async def monitor_status(websocket: WebSocket):
    with Session(engine) as session:
        statement = select(Toilet.name, Toilet.accessible, Toilet.watchdog)
        result = session.exec(statement).all()
        statuses = {}
        for name, accessible, watchdog in result:
            if not watchdog or datetime.datetime.now() - watchdog > datetime.timedelta(
                seconds=TIME_DELTA_WATCHDOG
            ):
                status = WS_STATUSES.unknown
            else:
                status = WS_STATUSES.free if accessible else WS_STATUSES.occupied
            statuses[name] = status.name

        await websocket.send_text(json.dumps(statuses))


app.include_router(api_router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

ui.run_with(
    app,
    mount_path="/",
    storage_secret="pick your private secret here",
    tailwind=True,
    title="CKJZ",
)
