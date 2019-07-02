from Core.cavernaEnums import ResourceTypeEnum
from BuisnessLogic.Effects import populationEffects, animalStorageEffect
from Core.baseTile import BaseTile

class WorkRoomTile(BaseTile):
	def __init__(self):
		self._name = "Work Room"
		self._id = 9
		self._isDwelling = False
		self._basePoints = 2
		self._cost = { ResourceTypeEnum.stone: 1 }
		self._effect = [boardEffects.FurnishTunnelsEffect()]
			
class GuestRoomTile(BaseTile):
	def __init__(self):
		self._name = "Guest Room"
		self._id = 10
		self._isDwelling = False
		self._basePoints = 0
		self._cost = {
			ResourceTypeEnum.wood: 1,
			ResourceTypeEnum.stone: 1 }
		self._effect = [actionEffects.ChangeDecisionVerb( ActionCombinationEnum.EitherOr, ActionCombinationEnum.AndOr )]
			
class OfficeRoomTile(BaseTile):
	def __init__(self):
		self._name = "Office Room"
		self._id = 11
		self._basePoints = 0
		self._isDwelling = True
		self._cost = { ResourceTypeEnum.stone: 1 }
		self._effect = [boardEffects.TwinTilesOverhangEffect()]