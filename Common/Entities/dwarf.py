from common.entities.weapon import Weapon


class Dwarf(object):
    def __init__(self, is_adult: bool = False):
        self._is_adult: bool = is_adult
        self._weapon: Weapon = None
        self._current_card: 'Card' = None

    @property
    def is_adult(self) -> bool:
        return self._is_adult

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    @property
    def has_weapon(self) -> bool:
        result = self._weapon is None
        return result

    @property
    def weapon_level(self) -> int:
        if self._weapon is None:
            return 0
        return self._weapon.level

    @property
    def is_active(self) -> bool:
        is_active = self._current_card is None
        return is_active

    @property
    def current_card_id(self) -> int:
        if self._current_card is None:
            return -1
        return self._current_card.id

    def make_adult(self):
        self._is_adult = True

    def give_weapon(self, weapon: Weapon):
        if self._weapon is not None:
            raise ValueError("dwarf already has a weapon")

        self._weapon = weapon

    def set_active(self, new_card):
        if new_card is None:
            raise ValueError("current card must not be none")

        if self._current_card is not None:
            raise ValueError("already active")

        self._current_card = new_card

    def clear_active_card(self):
        self._current_card = None
