from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.dwarf import Dwarf
from core.baseClasses.base_action import BaseAction
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer


class TakeAccumulatedItemsAction(BaseReceiveEventService, BaseAction):
    def __init__(self) -> None:
        BaseAction.__init__(self, "TakeAccumulatedItemsAction")

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Moves the resources from the active card to the player.

        :param player: The player who will receive the items. This cannot be null.
        :param active_card: The card which is providing the items. This cannot be null.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action, and the number of resources which were taken.
            This will never be null.
        """
        if player is None:
            raise ValueError("Player cannot be null.")
        if active_card is None:
            raise ValueError("Active Card cannot be null.")
        if not isinstance(active_card, ResourceContainer):
            raise ValueError("Active Card must be a resource container")

        result: ResultLookup[int] = self._give_player_resources(player, active_card.resources)
        active_card.clear_resources()

        return result

    def new_turn_reset(self):
        pass

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_spec):
        if "pp" in format_spec:
            return [("", "Take accumulated items")]
        return "Take accumulated items"

    def __repr__(self) -> str:
        return "TakeAccumulatedItemsAction()"
