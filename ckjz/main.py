from typing import Union

from fastapi import FastAPI

from ckjz import __version__

from ckjz.models.toilet import ToiletPublic, Toilet
from ckjz.engine import engine
from sqlmodel import Session, select

app = FastAPI(
    title="CKJZ",
    description="A simple API for the CKJZ project.",
    version=__version__,
)


@app.get("/toilets", response_model=list[ToiletPublic])
def display_toilets():
    with Session(engine) as session:
        toilets = session.exec(select(Toilet)).all()
        return toilets


@app.get("/toilets/{toilet_name}", response_model=ToiletPublic)
def display_toilet(toilet_name: str):
    with Session(engine) as session:
        toilet = session.exec(select(Toilet).where(Toilet.name == toilet_name)).first()
        return toilet


# @app.get("/healthz/{toilet_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}