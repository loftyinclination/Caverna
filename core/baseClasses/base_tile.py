from abc import ABCMeta
from typing import Dict, List, Optional, Tuple
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum, TileTypeEnum
from core.baseClasses.base_effect import BaseEffect


class BaseTile(metaclass=ABCMeta):

    def __init__(
            self,
            name: str,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_points: int = 0,
            cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects: Optional[List[BaseEffect]] = None):
        """Constructor for base Tile class.
        :param name: The name of the tile. This cannot be null.
        :param tile_id: The unique id of the tile.
        :param tile_type: The type of the tile.
        :param base_points: The number of points this tile is worth, without considering any effects. Defaults to zero.
        :param cost: The unaltered cost of purchasing the tile. If this is null, the tile is free.
        :param effects: The effects which the tile causes. If this is null, the tile has no effects.
        """
        if name is None or name.isspace():
            raise ValueError("tile name cannot be null or whitespace")
        self._name: str = name
        self._id: int = tile_id
        self._tile_type: TileTypeEnum = tile_type
        self._base_points: int = base_points

        if cost is None:
            cost = {}
        self._cost: Dict[ResourceTypeEnum, int] = cost

        if effects is None:
            effects = []
        self._effects: List[BaseEffect] = effects

    @property
    def is_dwelling(self) -> bool:
        return self._tile_type == TileTypeEnum.furnishedDwelling

    @property
    def tile_type(self) -> TileTypeEnum:
        return self._tile_type

    @property
    def base_points(self) -> int:
        return self._base_points

    @property
    def effects(self) -> List[BaseEffect]:
        return self._effects

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @property
    def cost(self) -> Dict[ResourceTypeEnum, int]:
        return self._cost


class BaseSpecificTile(BaseTile, metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            tile_id: int,
            tile_type: TileTypeEnum = TileTypeEnum.furnishedCavern,
            base_points: int = 0,
            cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects: Optional[List[BaseEffect]] = None,
            colour: TileColourEnum = TileColourEnum.Green):
        """Constructor for base Specific Tile class.
        :param name: The name of the tile. This cannot be null.
        :param tile_id: The unique id of the tile.
        :param tile_type: The type of the tile. For this subclass, this is defaulted to specific tile.
        :param cost: The unaltered cost of purchasing the tile. If this is null, the tile is free.
        :param effects: The effects which the tile causes. If this is null, the tile has no effects.
        :param colour: The colour of the tile.
        """
        BaseTile.__init__(
            self,
            name,
            tile_id,
            tile_type,
            base_points,
            cost,
            effects)
        self._colour: TileColourEnum = colour

    @property
    def colour(self) -> TileColourEnum:
        return self._colour


class BaseTwinTile(BaseTile):
    def __init__(
            self,
            name: str,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_points: int = 0,
            cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects: Optional[List[BaseEffect]] = None) -> None:
        BaseTile.__init__(
            self,
            name,
            tile_id,
            tile_type,
            base_points,
            cost,
            effects)
        self._location: Optional[Tuple[int, int]] = None

    @property
    def is_placed(self) -> bool:
        return self._location is not None

    @property
    def primary_tile_id(self) -> Optional[int]:
        if self.is_placed:
            return self._location[0]
        else:
            return None

    @property
    def secondary_tile_id(self) -> Optional[int]:
        if self.is_placed:
            return self._location[0]
        else:
            return None

    def place_tile(
            self,
            primary_location_id: int,
            secondary_location_id: int) -> bool:
        if self.is_placed:
            return False
        else:
            self._location = (primary_location_id, secondary_location_id)
            return True
