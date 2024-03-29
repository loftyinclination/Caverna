from buisness_logic.actions import receive_action
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum


class SuppliesCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Supplies", card_ids.SuppliesCardId,
            actions=receive_action.ReceiveAction({
                ResourceTypeEnum.wood: 1,
                ResourceTypeEnum.stone: 1,
                ResourceTypeEnum.ore: 1,
                ResourceTypeEnum.food: 1,
                ResourceTypeEnum.coin: 2}))
