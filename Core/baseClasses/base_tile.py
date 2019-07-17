from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum

class BaseTile(object):
    _name: str = "Uninitialised"
    _id: int = -1
    _isDwelling = False
    _cost: Dict[ResourceTypeEnum, int] = {}
    _basePoints: int = 0
    _effect = None