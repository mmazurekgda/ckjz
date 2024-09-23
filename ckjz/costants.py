import enum


class TOILET_TYPES(enum.Enum):
    UM1 = "UM1"
    UM2 = "UM2"
    UL1 = "UL1"
    UL2 = "UL2"
    GM = "GM"
    GL = "GL"


TOILETS = {
    # upper floor, men's room,
    # accessible from  the open space
    TOILET_TYPES.UM1: {
        "upper_floor": True,
        "ladies": False,
        "name": "UM1",
    },
    # upper floor, men's room,
    # accessible from the conference rooms
    TOILET_TYPES.UM2: {
        "upper_floor": True,
        "ladies": False,
        "name": "UM2",
    },
    # upper floor, ladies' room,
    # accessible from the open space
    TOILET_TYPES.UL1: {
        "upper_floor": True,
        "ladies": True,
        "name": "UL1",
    },
    # upper floor, ladies' room,
    # accessible from the conference rooms
    TOILET_TYPES.UL2: {
        "upper_floor": True,
        "ladies": True,
        "name": "UL2",
    },
    # ground floor, men's room
    TOILET_TYPES.GM: {
        "upper_floor": False,
        "ladies": False,
        "name": "GM",
    },
    # ground floor, ladies' room
    TOILET_TYPES.GL: {
        "upper_floor": False,
        "ladies": True,
        "name": "GL",
    },
}

COLORS = {
    "free": "rgba(84, 184, 72, 1.0)",
    "occupied": "rgba(255, 0, 0, 1.0)",
    "unknown": "rgba(150, 150, 150, 1.0)"
}

FAINT_COLORS = {
    "free": "rgba(84, 184, 72, 0.5)",
    "occupied": "rgba(255, 0, 0, 0.5)",
    "unknown": "rgba(70, 70, 70, 0.5)"
}

class WS_STATUSES(enum.Enum):
    occupied = "occupied"
    free = "free"
    unknown = "unknown"


TIME_DELTA_UPDATES = 1
TIME_DELTA_WATCHDOG = 10
