from core.baseClasses.base_card import BaseCard
from core.constants import card_ids


class ImitationCard(BaseCard):
    def __init__(
            self,
            amount_of_food: int) -> None:
        if amount_of_food < 0:
            raise ValueError("Amount of food must be greater than 0")
        self._amount_of_food: int = amount_of_food
        BaseCard.__init__(self, "Imitation", card_ids.ImitationCardId)

    @property
    def amount_of_food(self) -> int:
        return self._amount_of_food
