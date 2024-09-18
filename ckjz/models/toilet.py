from sqlmodel import SQLModel, Field
from typing import Optional
import datetime


class Toilet(SQLModel, table=True):
    __tablename__ = "toilets"
    id: int = Field(default=None, primary_key=True)
    upper_floor: bool
    ladies: bool
    name: str = Field(max_length=3, unique=True, index=True)
    accessible: Optional[bool] = False
    watchdog: Optional[datetime.datetime] = None


class ToiletPublic(SQLModel):
    id: Optional[int] = None
    upper_floor: bool
    ladies: bool
    name: str
    accessible: Optional[bool] = False
    watchdog: Optional[datetime.datetime] = None
