from typing import List, Tuple
from Core.cavernaEnums import TileDirectionEnum, TileTypeEnum
from Core.baseEffect import BaseEffect
from BuisnessLogic.Effects import boardEffects
from Core.baseTile import BaseTile
from Common.Services import TileContainerDefault, TileTwinDefault

class TileContainer(object):
	
	def __init__(self, height=6, width=8):
		if height < 0:
			raise ValueError("height must be greater than 0")
		if width < 0:
			raise ValueError("width must be greater than 0")
		self._height = height
		self._width = width
		
		self._tileCount = height * width
		
		twinDefault = TileTwinDefault.TileTwinDefault()
		self._twinTiles = twinDefault.Assign( [] )
		
		self._tiles: List[BaseTile] = []
		self._tilesType: Dict[int, TileTypeEnum] = {}
		if (height == 6 and width == 8):
			default = TileContainerDefault.TileContainerDefault()
			default.AssignInitialTiles( self._tilesType )
			
		self._tileRequisites: Dict[TileTypeEnum, List[TileTypeEnum]] = {
			TileTypeEnum.unavailable: [],
			TileTypeEnum.forest: [],
			TileTypeEnum.underground: [],
			TileTypeEnum.meadow: [TileTypeEnum.forest],
			TileTypeEnum.field: [TileTypeEnum.forest],
			TileTypeEnum.meadowFieldTwin: [TileTypeEnum.forest],
			TileTypeEnum.cavern: [TileTypeEnum.underground],
			TileTypeEnum.tunnel: [TileTypeEnum.underground],
			TileTypeEnum.deepTunnel: [TileTypeEnum.tunnel],
			TileTypeEnum.cavernTunnelTwin: [TileTypeEnum.underground],
			TileTypeEnum.cavernCavernTwin: [TileTypeEnum.underground],
			TileTypeEnum.pasture: [TileTypeEnum.field],
			TileTypeEnum.pastureTwin: [TileTypeEnum.field],
			TileTypeEnum.furnishedCavern: [TileTypeEnum.cavern],
			TileTypeEnum.furnishedDwelling: [TileTypeEnum.cavern],
			TileTypeEnum.oreMineDeepTunnelTwin: [TileTypeEnum.tunnel],
			TileTypeEnum.rubyMine: [TileTypeEnum.tunnel, TileTypeEnum.deepTunnel] }
		
	def GetTiles(self) -> List[BaseTile]:
		return self._tiles
		
	def GetEffects(self) -> List[BaseEffect]:
		effects = map(lambda tile: tile.GetEffects(), self._tiles)
		return list(effects)
		
	def GetEffectsOfType(self, type) -> List[BaseEffect]:
		result = [x for x in self.GetEffects() if isinstance(x, type)]
		return result
		
	def PlaceTile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
		if tile is None:
			raise ValueError("base tile")
			
		if location < 0 or location > 47:
			raise ValueError("base tile")
		
		if tile in self._twinTiles and direction is None:
			raise ValueError("direct cannot be null if tile is a twin tile")
			
		availableLocations = self.GetAvailableLocations( tile )
		if location in availableLocations:
			self._tiles.append( tile )
		
	def GetAvailableLocations(self, tile: TileTypeEnum) -> List[int]:
		effects = self.GetEffectsOfType( boardEffects.BaseBoardEffect )
		
		#gotta clone dictionary
		allTileRequisites = dict(self._tileRequisites)
		
		for effect in effects:
			effect.Invoke( allTileRequisites )
			
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
		
	def GetAdjacentTiles(self, location: int) -> List[Tuple[int, TileDirectionEnum]]:
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