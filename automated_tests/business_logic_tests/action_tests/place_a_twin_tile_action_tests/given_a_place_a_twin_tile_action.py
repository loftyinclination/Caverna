from abc import ABCMeta
from typing import cast, Dict, Optional
from unittest import TestCase

from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class Given_A_PlaceATwinTileAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PlaceATwinTileAction

        self.because()

    def initialise_sut_with_twin_tile(
            self,
            tile_type: TileTypeEnum = TileTypeEnum.oreMineDeepTunnelTwin,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None) -> None:
        self.SUT = PlaceATwinTileAction(tile_type, override_cost=override_cost)

    def because(self) -> None:
        pass

    def shouldNotBeEmpty(self, iterable) -> None:
        if isinstance(iterable, list):
            self.assertGreater(len(cast(list, iterable)), 0)
        else:
            self.assertGreater(len(list(iterable)), 0)