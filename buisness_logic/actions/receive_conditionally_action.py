from typing import Dict, Callable

from buisness_logic.actions.base_receive_action import BaseReceiveAction
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class ReceiveConditionallyAction(BaseReceiveAction):
    def __init__(
            self,
            condition: Callable[[BasePlayerRepository], int],
            items_to_receive: Dict[ResourceTypeEnum, int],
            condition_readable: str) -> None:
        if condition is None:
            raise ValueError("Condition cannot be null")
        if condition_readable is None or condition_readable.isspace():
            raise ValueError("condition_readable must not be null")

        self._condition: Callable[[BasePlayerRepository], int] = condition
        self._condition_readable: str = condition_readable

        BaseReceiveAction.__init__(self, "ReceiveConditionallyAction", items_to_receive)
        self._hash = self._precompute_hash()

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives the player some items proportional to how many times they fulfil the given condition.

        :param player: The player who will receive items. This cannot be null.
        :param active_card: Unused
        :param current_dwarf: Unused
        :return: A result lookup indicating the success of the action, and the number of resources which were given.
            This will never be null.
        """
        if player is None:
            raise ValueError("player")

        number_of_times_to_give: int = self._condition(player)

        resources_to_give: Dict[ResourceTypeEnum, int] = {r: self._items_to_receive[r] * number_of_times_to_give for r in self._items_to_receive}

        result: ResultLookup[int] = self._give_player_resources(player, resources_to_give)
        return result

    def new_turn_reset(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec):
        text = [("", "Receive ")]

        for (i, (resource, amount)) in enumerate(self._items_to_receive.items()):
            text.append(("class:count", str(amount)))
            text.append(("", " "))
            text.append(("class:resource", resource.name))
            if i != len(self._items_to_receive) - 1:
                text.append(("", ", "))

        text.append(("", " "))
        text.append(("", self._condition_readable))

        if "pp" in format_spec:
            return text
        return "".join(e[1] for e in text)

    def __repr__(self) -> str:
        result = "ReceiveConditionallyAction("
        count = 0
        for resource in self._items_to_receive:
            result += f"{resource.name}: {self._items_to_receive[resource]}"
            count += 1
            if count != len(self._items_to_receive):
                result += ", "
        result += ")"

        return result

    def _precompute_hash(self) -> int:
        return hash(("receive conditionally", self._condition, self._condition_readable, *self._items_to_receive))

    def __hash__(self) -> int:
        return self._hash
