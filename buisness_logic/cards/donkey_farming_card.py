from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class DonkeyFarmingCard(BaseResourceContainingCard):

    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Donkey Farming", card_ids.DonkeyFarmingCardId, 2,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                Conditional(
                    ActionCombinationEnum.AndOr,
                    Conditional(
                        ActionCombinationEnum.AndOr,
                        place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.pasture),
                        place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.pastureTwin)),
                    place_a_stable_action.PlaceAStableAction()),
                take_accumulated_items_action.TakeAccumulatedItemsAction()))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.donkey, 1)

        return self.resources
