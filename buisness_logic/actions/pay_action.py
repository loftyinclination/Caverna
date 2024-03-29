from typing import Dict, cast, Any

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.repositories.base_player_repository import BasePlayerRepository
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_action import BaseAction
from buisness_logic.actions.cannot_afford_action_error import CannotAffordActionError

class PayAction(BaseAction):
    def __init__(self, items_to_pay: Dict[ResourceTypeEnum, int], paying_for: Any):
        if items_to_pay is None:
            raise ValueError("Items to pay may not be null")
        for item in items_to_pay:
            if items_to_pay[item] < 0:
                raise ValueError(f"Cannot pay a negative amount of items (item: {item}, amount: {items_to_pay[item]})")
        self._items_to_pay: Dict[ResourceTypeEnum, int] = items_to_pay
        self._paying_for: Any = paying_for

        self._hash = self._precompute_hash()
        BaseAction.__init__(self, "PayAction", True, False, False)

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Allows the player to use an action which has already been claimed by another player.

        :param player: The player. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action.
            The flag will be false if the player does not have enough resources to pay the cost for this action.
            If true, the value is the number of paid resources.
            This will never be null.
        """
        if player is None:
            raise ValueError("Player cannot be null")

        if not player.has_more_resources_than(self._items_to_pay):
            return ResultLookup(errors=[CannotAffordActionError("Player", "to pay", self._items_to_pay, player.resources)])

        player.take_resources(self._items_to_pay)
        result = ResultLookup(True, sum(self._items_to_pay.values()))
        return result

    def new_turn_reset(self):
        pass

    def __str__(self) -> str:
        return "Pay " + ", ".join(f"{count} {resource.name}" for (resource, count) in self._items_to_pay.items())

    def __repr__(self):
        result = "PayAction("
        count = 0
        for resource in self._items_to_pay:
            result += f"{resource.name}: {self._items_to_pay[resource]}"
            count += 1
            if count != len(self._items_to_pay):
                result += ", "
        result += f", {self._paying_for!r})"
        return result

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, PayAction):
            return False
        cast_other: PayAction = cast(PayAction, other)

        return self._items_to_pay == cast_other._items_to_pay and self._paying_for == cast_other._paying_for

    def _precompute_hash(self) -> int:
        return hash(tuple(["Pay", *self._items_to_pay.items(), self._paying_for]))

    def __hash__(self) -> int:
        return self._hash
