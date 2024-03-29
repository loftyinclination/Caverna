from typing import Tuple, Dict, Optional
import logging

from buisness_logic.effects.food_effects import BaseFoodEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from buisness_logic.services.processor_services.animals_to_breed_action_choice_processor_service import AnimalsToBreedActionChoiceProcessorService
from buisness_logic.services.processor_services.card_action_choice_processor_service import CardActionChoiceProcessorService
from buisness_logic.services.processor_services.conversions_to_perform_action_choice_processor_service import ConversionsToPerformActionChoiceProcessorService
from buisness_logic.services.processor_services.expedition_reward_action_choice_processor_service import \
    ExpeditionRewardActionChoiceProcessorService
from buisness_logic.services.processor_services.market_items_to_purchase_action_choice_processor_service import \
    MarketItemsToPurchaseActionChoiceProcessorService
from buisness_logic.services.processor_services.resource_to_sow_action_choice_processor_service import ResourceToSowActionChoiceProcessorService
from buisness_logic.services.processor_services.specific_tile_placement_action_choice_processor_service import SpecificTilePlacementActionChoiceProcessorService
from buisness_logic.services.processor_services.stable_placement_action_choice_processor_service import StablePlacementActionChoiceProcessorService
from buisness_logic.services.processor_services.tile_and_placement_action_choice_processor_service import TileAndPlacementActionChoiceProcessorService
from buisness_logic.services.processor_services.tile_purchase_effect_action_choice_processor_service import \
    TilePurchaseEffectActionChoiceProcessorService
from buisness_logic.services.processor_services.twin_tile_placement_action_choice_processor_service import TwinTilePlacementActionChoiceProcessorService
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.resources_to_sow_lookup import ResourcesToSow
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.tile_service import TileService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.services.base_action_choice_processor_service import BaseActionChoiceProcessorService
from core.services.base_player_service import BasePlayerService, InvalidActionCombinationResponse


class ActionChoicePlayerService(BasePlayerService):
    def __init__(
            self,
            player_id: int,
            player_descriptor: str,
            player_turn_index: int) -> None:
        logging.info(f"Initialising ActionChoicePlayer {player_descriptor}")
        BasePlayerService.__init__(
            self,
            player_id,
            player_descriptor,
            player_turn_index,
            TileContainerDefault())
        self._card_action_choice_processor_service: CardActionChoiceProcessorService = CardActionChoiceProcessorService()
        self._tile_and_placement_action_choice_processor_service: TileAndPlacementActionChoiceProcessorService = TileAndPlacementActionChoiceProcessorService()
        self._specific_tile_placement_action_choice_processor_service: SpecificTilePlacementActionChoiceProcessorService = \
            SpecificTilePlacementActionChoiceProcessorService()
        self._twin_tile_placement_action_choice_processor_service: TwinTilePlacementActionChoiceProcessorService = \
            TwinTilePlacementActionChoiceProcessorService()
        self._stable_placement_action_choice_processor_service: StablePlacementActionChoiceProcessorService = StablePlacementActionChoiceProcessorService()
        self._expedition_reward_action_choice_processor_service: ExpeditionRewardActionChoiceProcessorService = ExpeditionRewardActionChoiceProcessorService()
        self._tile_purchase_effect_action_choice_processor_service: TilePurchaseEffectActionChoiceProcessorService = \
            TilePurchaseEffectActionChoiceProcessorService()
        self._resource_to_sow_action_choice_processor_service: ResourceToSowActionChoiceProcessorService = ResourceToSowActionChoiceProcessorService()
        self._market_items_to_purchase_action_choice_processor_service: MarketItemsToPurchaseActionChoiceProcessorService = \
            MarketItemsToPurchaseActionChoiceProcessorService()
        self._animals_to_breed_action_choice_processor_service: AnimalsToBreedActionChoiceProcessorService = AnimalsToBreedActionChoiceProcessorService()
        self._conversions_to_perform_action_choice_processor_service: ConversionsToPerformActionChoiceProcessorService = \
            ConversionsToPerformActionChoiceProcessorService()

        self._tile_service: TileService = TileService()

        self._processor_services: list[BaseActionChoiceProcessorService] = [
            self._card_action_choice_processor_service,
            self._tile_and_placement_action_choice_processor_service,
            self._specific_tile_placement_action_choice_processor_service,
            self._twin_tile_placement_action_choice_processor_service,
            self._stable_placement_action_choice_processor_service,
            self._expedition_reward_action_choice_processor_service,
            self._tile_purchase_effect_action_choice_processor_service,
            self._resource_to_sow_action_choice_processor_service,
            self._market_items_to_purchase_action_choice_processor_service,
            self._animals_to_breed_action_choice_processor_service,
            self._conversions_to_perform_action_choice_processor_service,
        ]

        current_total: int = 0
        for service in self._processor_services:
            service.offset = current_total
            current_total += service.length

        self._action_choice_length: int = current_total

    def _set_action_choice_for_turn(
            self,
            action_choice: list[int]) -> None:
        if action_choice is None:
            raise ValueError("Action choice may not be None")
        if len(action_choice) != self._action_choice_length:
            raise ValueError(f"Action choice is not of correct length (actual={len(action_choice)}, expected={self._action_choice_length})")
        for service in self._processor_services:
            service.set_action_choice(action_choice)

    def _set_action_choice_if_unset(self, turn_descriptor) -> None:
        if len(self._processor_services[0]._action_choice) != 0:
            return
        raise NotImplementedError("need to turn turn descriptor into observations?")

    def report_action_choice_failed(
            self,
            actions) -> InvalidActionCombinationResponse:
        raise NotImplementedError()

    def get_player_choice_conversions_to_perform(
            self,
            turn_descriptor: TurnDescriptorLookup) -> list[Tuple[list[ResourceTypeEnum], int, list[ResourceTypeEnum]]]:
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor cannot be none")
        self._set_action_choice_if_unset(turn_descriptor)

        conversions_to_perform: list[Tuple[list[ResourceTypeEnum], int, list[ResourceTypeEnum]]]
        _, conversions_to_perform = self._conversions_to_perform_action_choice_processor_service.process_action_choice_conversions_to_perform()

        return conversions_to_perform

    def get_player_choice_market_items_to_purchase(
            self,
            _unused_market_choices,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[list[ResourceTypeEnum]]:
        self._set_action_choice_if_unset(turn_descriptor)

        items_to_purchase: list[ResourceTypeEnum]
        _, items_to_purchase = self._market_items_to_purchase_action_choice_processor_service.process_action_choice_for_market_items()
        result: ResultLookup[list[ResourceTypeEnum]] = ResultLookup(True, items_to_purchase)
        return result

    def get_player_choice_weapon_level(
            self,
            turn_descriptor: TurnDescriptorLookup) -> int:
        raise NotImplementedError()

    def get_player_choice_animals_to_breed(
            self,
            animals_which_can_reproduce: list[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[list[ResourceTypeEnum]]:
        self._set_action_choice_if_unset(turn_descriptor)

        animals_to_breed: list[ResourceTypeEnum]
        _, animals_to_breed = self._animals_to_breed_action_choice_processor_service.process_action_choice_for_animals_to_breed(
            possible_number_of_animals_to_reproduce)
        result: ResultLookup[list[ResourceTypeEnum]] = ResultLookup(True, animals_to_breed)
        return result

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: list[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[bool]:
        self._set_action_choice_if_unset(turn_descriptor)

        use_dwarf_out_of_order: bool
        _, use_dwarf_out_of_order = self._card_action_choice_processor_service.process_action_choice_use_dwarf_out_of_order()
        result: ResultLookup[bool] = ResultLookup(True, use_dwarf_out_of_order)
        return result

    def get_player_choice_use_card_already_in_use(
            self,
            unused_available_cards: list[BaseCard],
            used_available_cards: list[BaseCard],
            amount_of_food_required: int,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        raise NotImplementedError()

    def get_player_choice_card_to_use(
            self,
            available_cards: list[BaseCard],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        if len(available_cards) == 0:
            raise ValueError("Must have at least one available card")
        self._set_action_choice_if_unset(turn_descriptor)

        card_id: int
        _, card_id = self._card_action_choice_processor_service.process_action_choice_card()

        is_card_available: bool = False
        # noinspection PyTypeChecker
        card: BaseCard = None
        for card in available_cards:
            if card.id == card_id:
                is_card_available = True
                break

        result: ResultLookup[BaseCard]
        if is_card_available:
            result = ResultLookup(True, card)
        else:
            result = ResultLookup(errors=f"Chosen card {card_id} was not available")
        return result

    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: list[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        self._set_action_choice_if_unset(turn_descriptor)

        dwarf_to_use_out_of_order: int
        _, dwarf_to_use_out_of_order = self._card_action_choice_processor_service.process_action_choice_use_dwarf_out_of_order()

        result: ResultLookup[Dwarf]
        if dwarf_to_use_out_of_order < len(dwarves):
            dwarves = sorted(dwarves, key=lambda d: d.weapon_level)
            dwarf_to_use: Dwarf = dwarves[dwarf_to_use_out_of_order]
            result = ResultLookup(True, dwarf_to_use)
        else:
            result = ResultLookup(errors=f"Chosen dwarf {dwarf_to_use_out_of_order} was not available: only {len(dwarves)} to choose from.")
        return result

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: list[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        self._set_action_choice_if_unset(turn_descriptor)

        actions_to_use: ActionChoiceLookup
        _, actions_to_use = self._card_action_choice_processor_service.process_action_choice_action()

        is_action_choice_valid: bool = False
        # noinspection PyTypeChecker
        action_choice: ActionChoiceLookup = None
        for action_choice in available_action_choices:
            if action_choice == actions_to_use:
                is_action_choice_valid = True

        result: ResultLookup[ActionChoiceLookup]
        if is_action_choice_valid:
            result = ResultLookup(True, action_choice)
        else:
            result = ResultLookup(errors="Action choice is invalid")

        return result

    def get_player_choice_free_actions_to_use(
            self,
            turn_descriptor: TurnDescriptorLookup) -> list[BaseAction]:
        raise NotImplementedError()

    def get_player_choice_fences_to_build(
            self,
            place_pasture_action: BaseAction,
            place_twin_pasture_action: BaseAction,
            place_stable_action: Optional[BaseAction],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[list[BaseAction]]:
        raise NotImplementedError()

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: list[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        if possible_tiles is None:
            raise ValueError("Possible tiles may not be none")
        if len(possible_tiles) == 0:
            raise ValueError("Must have at least one possible tile")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")
        self._set_action_choice_if_unset(turn_descriptor)

        possible_tiles_by_id: Dict[int, BaseTile] = {tile.id: tile for tile in possible_tiles}
        tile_id: int
        _, __, tile_id = self._tile_and_placement_action_choice_processor_service.process_action_choice_tile_and_placement()

        result: ResultLookup[BaseTile]
        if tile_id in possible_tiles_by_id:
            result = ResultLookup(True, possible_tiles_by_id[tile_id])
        else:
            result = ResultLookup(errors=f"Attempted to choose tile with id {tile_id} but it was not available")
        return result

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: list[BaseAction],
            expedition_level: int,
            is_first_expedition_action: bool,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[list[BaseAction]]:
        if possible_expedition_rewards is None:
            raise ValueError("Possible rewards may not be none")
        if len(possible_expedition_rewards) == 0:
            raise ValueError("Must have at least one possible expedition reward")
        if expedition_level < 1:
            raise ValueError("Expedition level must be positive")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")
        self._set_action_choice_if_unset(turn_descriptor)

        rewards: list[BaseAction]
        _, rewards = self._expedition_reward_action_choice_processor_service.process_action_choice_placement_for_rewards(
            expedition_level,
            is_first_expedition_action,
            possible_expedition_rewards)

        result: ResultLookup[list[BaseAction]]
        if len(rewards) > expedition_level:
            result = ResultLookup(errors=f"Can only pick {expedition_level} rewards -- chose {len(rewards)}")
        else:
            result = ResultLookup(True, rewards)

        return result

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        if tile is None:
            raise ValueError("Tile may not be none")
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")
        self._set_action_choice_if_unset(turn_descriptor)

        location: int
        if self._tile_service.does_tile_type_have_unique_tile(tile.tile_type):
            _, location = self._specific_tile_placement_action_choice_processor_service.process_action_choice_placement_for_tile(tile)
        else:
            _, location, __ = self._tile_and_placement_action_choice_processor_service.process_action_choice_tile_and_placement()
        result: ResultLookup[int] = ResultLookup(True, location)
        return result

    def get_player_choice_location_to_build_twin(
            self,
            tile_type: TileTypeEnum,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[TileTwinPlacementLookup]:
        if turn_descriptor is None:
            raise ValueError("Turn Descriptor may not be none")
        self._set_action_choice_if_unset(turn_descriptor)

        placement: TileTwinPlacementLookup
        _, placement = self._twin_tile_placement_action_choice_processor_service.process_action_choice_placement_for_tile(tile_type)

        result: ResultLookup[TileTwinPlacementLookup] = ResultLookup(True, placement)
        return result

    def get_player_choice_location_to_build_stable(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[int]:
        self._set_action_choice_if_unset(turn_descriptor)

        location: int
        _, location = self._stable_placement_action_choice_processor_service.process_action_choice_placement_for_stable()

        result: ResultLookup[int] = ResultLookup(True, location)
        return result

    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            tile_cost: Dict[ResourceTypeEnum, int],
            possible_effects: list[BaseTilePurchaseEffect],
            turn_descriptor: TurnDescriptorLookup) -> Dict[BaseTilePurchaseEffect, int]:
        self._set_action_choice_if_unset(turn_descriptor)

        return self._tile_purchase_effect_action_choice_processor_service.process_action_choice_purchase_effects()

    def get_player_choice_use_harvest_action_instead_of_breeding(
            self,
            turn_descriptor: TurnDescriptorLookup) -> bool:
        raise NotImplementedError()

    def get_player_choice_effect_to_use_for_feeding_dwarves(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[list[BaseFoodEffect]]:
        raise NotImplementedError()

    def get_player_choice_resources_to_sow(
            self,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ResourcesToSow]:
        self._set_action_choice_if_unset(turn_descriptor)

        resources_to_sow: list[ResourceTypeEnum]
        _, resources_to_sow = self._resource_to_sow_action_choice_processor_service.process_action_choice_for_resources_to_sow()

        result: ResultLookup[list[ResourceTypeEnum]] = ResultLookup(True, resources_to_sow)
        return result
