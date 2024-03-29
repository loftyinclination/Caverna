from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum


class AdventureCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Adventure", card_ids.AdventureCardId, 4,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                give_dwarf_a_weapon_action.GiveDwarfAWeaponAction(),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    go_on_an_expedition_action.GoOnAnExpeditionAction(1),
                    go_on_an_expedition_action.GoOnAnExpeditionAction(1, False))))
