from typing import List, Dict, TypeVar, Generic, cast, Optional

from common.defaults.tile_container_default import TileContainerDefault
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum

T = TypeVar('T')


class TileContainer(object):
    def __init__(
            self,
            height: int = 6,
            width: int = 8):
        if height < 0:
            raise ValueError("height must be greater than 0")
        if width < 0:
            raise ValueError("width must be greater than 0")
        self._height: int = height
        self._width: int = width

        self._tileCount: int = height * width

        self._tiles: Dict[int, TileEntity] = {}
        if height == 6 and width == 8:
            default: TileContainerDefault = TileContainerDefault()
            default.assign(self._tiles)
        else:
            print("Unknown board dimensions")

    def get_number_of_tiles_of_type(self, tile_type: TileTypeEnum) -> int:
        return len([t for t in self._tiles.values() if t.tile_type == tile_type])

    @property
    def tile_count(self) -> int:
        return self._tileCount

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def tiles(self) -> Dict[int, TileEntity]:
        """Get the tiles contained in this container"""
        return self._tiles

    def get_tile_at_location(self, tile_index: int) -> TileEntity:
        if tile_index < 0 or tile_index >= self._tileCount:
            raise IndexError(f"Tile Index ({tile_index}) must be in range [0, Number of Tiles: {self._tileCount})")
        return self._tiles[tile_index]

    def get_tiles_of_type(
            self,
            base_tile_type: Generic[T]) -> List[T]:
        """Get the (base tiles) tiles which extend some base type."""
        result = [cast(base_tile_type, x.tile) for x in self._tiles.values() if isinstance(x.tile, base_tile_type)]
        return result

    def get_specific_tile_at_location(
            self,
            tile_index: int) -> Optional[BaseTile]:
        """Get the tile at the given location

        :param tile_index: The location to get the tile for. This must be in the range [0, self._tileCount).
        :return: The base tile at the given location, if it exists. If there is no tile, the result will be none."""
        if tile_index < 0 or tile_index > self._tileCount:
            raise ValueError()
        return self._tiles.get(tile_index, None).tile

    @property
    def effects(self) -> List[BaseEffect]:
        """Get a list of all the effects held by any tile in this container"""
        effects = [effect for tile in self._tiles.values() for effect in tile.effects]

        return effects

    def get_effects_of_type(
            self,
            effect_type: Generic[T]) -> List[T]:
        """Get a list of all of the effects which extend a certain base effect in this container"""
        if effect_type is None:
            raise ValueError("Effect Type may not be none")
        result = [x for x in self.effects if isinstance(x, effect_type)]
        return result
