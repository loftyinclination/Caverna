from typing import List, Tuple
from core.enums.caverna_enums import TileDirectionEnum, TileTypeEnum
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from buisness_logic.effects import board_effects
from common.defaults import tile_container_default, tile_twin_default

class TileContainer(object):
    
    def __init__(self, height=6, width=8):
        if height < 0:
            raise ValueError("height must be greater than 0")
        if width < 0:
            raise ValueError("width must be greater than 0")
        self._height = height
        self._width = width
        
        self._tileCount = height * width
        
        twinDefault = tileTwinDefault.TileTwinDefault()
        self._twinTiles = twinDefault.assign( [] )
        
        self._tiles: Dict[int, TileEntity] = []
        if ( height == 6 and width == 8):
            default = TileContainerDefault.TileContainerDefault()
            default.AssignInitialTiles( self._tiles )
            
        requisiteDefault = tileRequisiteDefault.TileRequisiteDefault()
        self._tileRequisites: Dict[TileTypeEnum, List[TileTypeEnum]] = requisiteDefault.assign( {} )
        
    def get_tiles(self) -> List[BaseTile]:
        '''Get the base tiles contained in this container'''
        result = [x.get_tile() for x in self._tiles if x.get_tile() is not None]
        return result
        
    def get_effects(self) -> List[BaseEffect]:
        '''Get a list of all the effects held by any tile in this container'''
        effects = map(lambda tile: tile.GetEffects(), self._tiles)
        effects = map(lambda tile: tile.GetEffects(), self.get_tiles())
        return list(effects)
        
    def get_effects_of_type(self, type) -> List[BaseEffect]:
        '''Get a list of all of the effects which extend a certain base effect in this container'''
        result = [x for x in self.GetEffects() if isinstance(x, type)]
        return result
        
    def place_tile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
        '''Place a tile in this container
        
        Input:
        '''
        if tile is None:
            raise ValueError("base tile")
            
        if location < 0 or location > 47:
            raise ValueError("base tile")
        
        if tile in self._twinTiles and direction is None:
            raise ValueError("direct cannot be null if tile is a twin tile")
            
        availableLocations = self.GetAvailableLocations( tile )
        if location in availableLocations:
            self._tiles.append( tile )
        
    def get_available_locations(self, tile: TileTypeEnum) -> List[int]:
        effects = self.GetEffectsOfType( boardEffects.BaseBoardEffect )
        
        #gotta clone dictionary
        allTileRequisites = dict(self._tileRequisites)
        
        for effect in effects:
            effect.invoke( allTileRequisites )
            
        #get the correct requisites -- if adjacent, allow unavailable
        tileRequisites: List[TileTypeEnum] = allTileRequisites[ tile ]
        
        #filter _tilesType by new requisites
        validPositions: List[int] = [x for x in self._tilesType if self._tilesType[x] in tileRequisites]
        
        #if twin, check all requisites for adjacent
        if tile in self._twinTiles:
            validPositionsWithAdjacent: List[Tuple[int, TileDirectionEnum]] = []
            for position in validPositions:
                adjacentTiles: List[Tuple[int, TileDirectionEnum]] = self.GetAdjacentTiles( position )
                for adjacentTile in adjacentTiles:
                    if self._tilesType[adjacentTile[0]] in tileRequisites:
                        validPositionsWithAdjacent.append( (position, adjacentTile[1]) )
                        break
            return list(map(lambda validPositionWithAdjacent: validPositionWithAdjacent[0], validPositionsWithAdjacent))
                    
        return validPositions
        #only unavailable with adjacent (in correct section) will pass both checks
        
    def get_adjacent_tiles(self, location: int) -> List[Tuple[int, TileDirectionEnum]]:
        if location < 0 or location > self._tileCount:
            raise ValueError
    
        directionOffset = {
            TileDirectionEnum.up: -8,
            TileDirectionEnum.down: 8,
            TileDirectionEnum.left: -1,
            TileDirectionEnum.right: 1 }
        
        adjacentDirectionCondition = {
            TileDirectionEnum.up: lambda adjloc: adjloc > 0,
            TileDirectionEnum.down: lambda adjloc: adjloc < self._tileCount,
            TileDirectionEnum.left: lambda adjloc: adjloc % self._width != 7,
            TileDirectionEnum.right: lambda adjloc: adjloc % self._width != 0 }
        
        result = []
        
        for x in directionOffset:
            adjacentLocation = location + directionOffset[x]
            if adjacentDirectionCondition[x]( adjacentLocation ):
                result.append( (adjacentLocation, x) )
                
        return result
