from typing import List, NamedTuple, Tuple, Optional

from buisness_logic.services.base_action_player_choice_transfer_service import BaseActionPlayerChoiceTransferService
from buisness_logic.services.base_card_player_choice_transfer_service import BaseCardPlayerChoiceTransferService
from buisness_logic.services.base_dwarf_player_choice_transfer_service import BaseDwarfPlayerChoiceTransferService
from buisness_logic.services.complete_action_player_choice_transfer_service import CompleteActionPlayerChoiceTransferService
from buisness_logic.services.complete_card_player_choice_transfer_service import CompleteCardPlayerChoiceTransferService
from buisness_logic.services.complete_dwarf_player_choice_transfer_service import CompleteDwarfPlayerChoiceTransferService
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.dwarf_card_action_combination_lookup import DwarfCardActionCombinationLookup
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.conditional_service import ConditionalService
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.services.base_player_service import BasePlayerService


class ChosenDwarfCardActionCombinationAndEquivalentLookup(NamedTuple):
    choice: Optional[DwarfCardActionCombinationLookup]
    equivalents: List[DwarfCardActionCombinationLookup]


class TurnTransferService(object):
    def __init__(self):
        self._conditional_service: ConditionalService = ConditionalService()

        self._dwarf_transfer_service: BaseDwarfPlayerChoiceTransferService = CompleteDwarfPlayerChoiceTransferService()
        self._card_transfer_service: BaseCardPlayerChoiceTransferService = CompleteCardPlayerChoiceTransferService()
        self._action_transfer_service: BaseActionPlayerChoiceTransferService = CompleteActionPlayerChoiceTransferService()

    def get_turn(
            self,
            player: BasePlayerService,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup]:
        if player is None:
            raise ValueError("Player may not be null.")
        if turn_descriptor is None:
            raise ValueError("Turn descriptor may not be null.")
        if turn_descriptor.turn_index >= len(player.dwarves):
            raise IndexError(f"Turn Index ({turn_descriptor.turn_index}) must be less than number of dwarves ({len(player.dwarves)})")

        success: bool = False
        choice: Optional[DwarfCardActionCombinationLookup] = None
        equivalents: List[DwarfCardActionCombinationLookup] = []
        errors: List[str] = []

        dwarf_result: ResultLookup[Tuple[Dwarf, ActionChoiceLookup]] = self._dwarf_transfer_service \
            .get_dwarf(
                player,
                turn_descriptor)

        chosen_dwarf: Dwarf
        dwarf_action_choice: ActionChoiceLookup
        chosen_dwarf, dwarf_action_choice = dwarf_result.value

        errors.extend(dwarf_result.errors)

        if dwarf_result.flag:
            card_result: ResultLookup[Tuple[BaseCard, ActionChoiceLookup]] = self._card_transfer_service \
                .get_card(
                    player,
                    chosen_dwarf,
                    turn_descriptor)

            chosen_card: BaseCard
            card_action_choice: ActionChoiceLookup
            chosen_card, card_action_choice = card_result.value

            errors.extend(card_result.errors)

            if card_result.flag:
                action_result: ResultLookup[ActionChoiceLookup] = self._action_transfer_service \
                    .get_action(
                        player,
                        chosen_dwarf,
                        chosen_card,
                        turn_descriptor)

                errors.extend(action_result.errors)

                if action_result.flag:
                    action_action_choice = action_result.value

                    actions: List[BaseAction] = []
                    actions.extend(dwarf_action_choice.actions)
                    actions.extend(card_action_choice.actions)
                    actions.extend(action_action_choice.actions)

                    constraints: List[BaseConstraint] = []
                    constraints.extend(dwarf_action_choice.constraints)
                    constraints.extend(card_action_choice.constraints)
                    constraints.extend(action_action_choice.constraints)

                    for dwarf_action in dwarf_action_choice.actions:
                        for card_action in card_action_choice.actions:
                            constraint: BaseConstraint = PrecedesConstraint(dwarf_action, card_action)
                            constraints.append(constraint)

                        for action_action in action_action_choice.actions:
                            constraint: BaseConstraint = PrecedesConstraint(dwarf_action, action_action)
                            constraints.append(constraint)

                    for card_action in card_action_choice.actions:
                        for action_action in action_action_choice.actions:
                            constraint: BaseConstraint = PrecedesConstraint(card_action, action_action)
                            constraints.append(constraint)

                    choice = DwarfCardActionCombinationLookup(
                        chosen_dwarf,
                        chosen_card,
                        ActionChoiceLookup(actions, constraints))

                    success = True
            else:
                equivalent_cards: List[BaseCard] = self.get_equivalent_invalid_cards(player, chosen_dwarf, chosen_card)
                card: BaseCard
                for card in equivalent_cards:
                    possible_choices: List[ActionChoiceLookup] = self._conditional_service.get_possible_choices(card.actions, player)
                    action_choice: ActionChoiceLookup
                    for action_choice in possible_choices:
                        new_equivalent: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
                            chosen_dwarf,
                            card,
                            action_choice)
                        equivalents.append(new_equivalent)
        else:
            equivalent_dwarves: List[Dwarf] = self.get_equivalent_invalid_dwarves(player, chosen_dwarf)
            dwarf: Dwarf
            for dwarf in equivalent_dwarves:
                card: BaseCard
                for card in turn_descriptor.cards:
                    possible_choices: List[ActionChoiceLookup] = self._conditional_service.get_possible_choices(card.actions)
                    action_choice: ActionChoiceLookup
                    for action_choice in possible_choices:
                        new_equivalent: DwarfCardActionCombinationLookup = DwarfCardActionCombinationLookup(
                            dwarf,
                            card,
                            action_choice)
                        equivalents.append(new_equivalent)

        data: ChosenDwarfCardActionCombinationAndEquivalentLookup = ChosenDwarfCardActionCombinationAndEquivalentLookup(
            choice,
            equivalents)
        result: ResultLookup[ChosenDwarfCardActionCombinationAndEquivalentLookup] = ResultLookup(success, data, errors)
        return result

    def get_equivalent_invalid_dwarves(
            self,
            player: BasePlayerService,
            chosen_dwarf: Dwarf) -> List[Dwarf]:
        result: List[Dwarf]

        if chosen_dwarf.is_active:
            result = [dwarf for dwarf in player.dwarves if dwarf.is_active]
        else:
            result = [chosen_dwarf]

        return result

    def get_equivalent_invalid_cards(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            card: BaseCard) -> List[BaseCard]:
        # TODO: Implement this
        return []
