from Core.cavernaEnums import ResourceTypeEnum, TileTypeEnum
from Core.baseTile import BaseTile
from Common.Entities import weapon

class CarpenterTile(BaseTile):
	def __init__(self):
		self._name = "Carpenter"
		self._id = 12
		self._isDwelling = False
		self._basePoints = 0
		self._cost = { ResourceTypeEnum.stone: 1 }
		self._effect = [ purchaseEffect.DecreasePrice( {ResourceTypeEnum.wood: 1}, BaseTile ) ]
			
class StoneCarverTile(BaseTile):
	def __init__(self):
		self._name = "Stone Carver"
		self._id = 13
		self._isDwelling = False
		self._basePoints = 1
		self._cost = { ResourceTypeEnum.wood: 1 }
		self._effect = [
			resourceEffect.Receive( {ResourceTypeEnum.stone: 2} ),
			purchaseEffect.DecreasePrice( {ResourceTypeEnum.stone: 1}, BaseTile ) ]

class BlacksmithTile(BaseTile):
	def __init__(self):
		self._name = "Blacksmith"
		self._id = 14
		self._isDwelling = False
		self._basePoints = 3
		self._cost = {
			ResourceTypeEnum.wood: 1,
			ResourceTypeEnum.stone: 2 }
		self._effect = [
			resourceEffect.Receive( {ResourceTypeEnum.ore: 2} ),
			purchaseEffect.DecreasePrice( {ResourceTypeEnum.ore: 2}, weapon.Weapon ) ]
			
class BuilderTile(BaseTile):
	def __init__(self):
		self._name = "Blacksmith"
		self._id = 14
		self._isDwelling = False
		self._basePoints = 3
		self._cost = {
			ResourceTypeEnum.wood: 1,
			ResourceTypeEnum.stone: 2 }
		self._effect = [
			resourceEffect.Receive( {ResourceTypeEnum.ore: 2} ),
			purchaseEffect.DecreasePrice( {ResourceTypeEnum.ore: 2}, weapon.Weapon ) ]
		