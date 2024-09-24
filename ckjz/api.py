import datetime
import logging
from ckjz.models.toilet import ToiletPublic, Toilet
from ckjz.engine import engine
from sqlmodel import Session, select
from fastapi import APIRouter

router = APIRouter(prefix="/toilets", tags=["toilets"])


@router.get("/", response_model=list[ToiletPublic])
def display_toilets():
    with Session(engine) as session:
        toilets = session.exec(select(Toilet)).all()
        return toilets


@router.get("/{toilet_name}", response_model=ToiletPublic)
def display_toilet(toilet_name: str):
    with Session(engine) as session:
        toilet = session.exec(select(Toilet).where(Toilet.name == toilet_name)).first()
        return toilet


@router.post("/{toilet_name}", response_model=ToiletPublic)
def update_toilet(toilet_name: str, status: bool):
    logger = logging.getLogger(__name__)
    with Session(engine) as session:
        toilet = session.exec(select(Toilet).where(Toilet.name == toilet_name)).first()
        if not toilet:
            logger.error(f"Toilet `{toilet_name}` not found")
            return None
        toilet.accessible = status
        toilet.watchdog = datetime.datetime.now()
        session.add(toilet)
        session.commit()
        session.refresh(toilet)
        return toilet
