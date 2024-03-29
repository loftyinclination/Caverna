from typing import List

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.repositories.base_player_repository import BasePlayerRepository


class UpgradeDwarfWeaponAction(BaseAction):
    def __init__(self) -> None:
        self._hash = hash("upgrade dwarf weapon")
        BaseAction.__init__(self, "UpgradeDwarfWeaponAction", False, False, True)

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

        if current_dwarf.has_weapon:
            increase_level_result: ResultLookup[int] = current_dwarf.weapon.increase_level()
            if increase_level_result.flag:
                successes += 1
            else:
                for error in increase_level_result.errors:
                    errors.append(error)

        # TODO: Consider changing the success value of this -- may cause failures.
        result: ResultLookup[int] = ResultLookup(successes > 0, successes, errors)
        return result

    def new_turn_reset(self):
        pass

    def __eq__(self, other) -> bool:
        return isinstance(other, UpgradeDwarfWeaponAction)

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return "UpgradeDwarfWeaponAction()"
