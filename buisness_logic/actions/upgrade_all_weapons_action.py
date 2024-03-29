from typing import List

from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class UpgradeAllWeaponsAction(BaseAction):
    def __init__(self) -> None:
        self._hash = hash("upgrade all weapons")
        BaseAction.__init__(self, "UpgradeAllWeaponsAction", True, False, True)

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Increases the level of all weapons owned by dwarves.

        :param player: The player who has dwarves. This may not be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action.
            The flag will be false if no dwarves have weapons to upgrade.
            The value indicates the number of dwarves which have had weapons upgraded.
            This will never be null.
        """
        if player is None:
            raise ValueError(str(player))
        successes: int = 0
        errors: List[str] = []

        for dwarf in player.dwarves:
            if not dwarf.has_weapon:
                continue
            increase_level_result: ResultLookup[int] = dwarf.weapon.increase_level()
            errors.extend(increase_level_result.errors)

            if increase_level_result.flag:
                successes += 1

        result: ResultLookup[int] = ResultLookup(len(errors) == 0, successes, errors)
        return result

    def new_turn_reset(self):
        pass

    def __eq__(self, other) -> bool:
        return isinstance(other, UpgradeAllWeaponsAction)

    def __hash__(self) -> int:
        return 1

    def __str__(self) -> str:
        return "Upgrade All Weapons"

    def __repr__(self) -> str:
        return "UpgradeAllWeaponsAction()"

    def __hash__(self) -> int:
        return self._hash
