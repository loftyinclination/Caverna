from typing import List

from automated_tests.business_logic_tests.service_tests.processor_service_tests.market_items_processor_service_tests.given_a_market_items_to_purchase_action_choice_processor_service import \
    Given_A_MarketItemsToPurchaseActionChoiceProcessorService
from buisness_logic.services.processor_services.market_items_to_purchase_action_choice_processor_service import MarketItemActionChoice
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_no_probability_is_above_threshold(Given_A_MarketItemsToPurchaseActionChoiceProcessorService):
    def because(self) -> None:
        #  0: ResourceTypeEnum.dog,
        #  1: ResourceTypeEnum.sheep,
        #  2: ResourceTypeEnum.donkey,
        #  3: ResourceTypeEnum.boar,
        #  4: ResourceTypeEnum.cow,
        #  5: ResourceTypeEnum.wood,
        #  6: ResourceTypeEnum.stone,
        #  7: ResourceTypeEnum.ore,
        #  8: ResourceTypeEnum.grain,
        #  9: ResourceTypeEnum.veg,
        action_choice: List[float] = [0.1 for _ in range(self.SUT.length)]
        action_choice[4] = 0.6
        action_choice[6] = 0.8
        action_choice[9] = 0.7

        self.SUT.set_action_choice(action_choice)

        self._result: MarketItemActionChoice = self.SUT.process_action_choice_for_market_items()
        self._expected_items_to_purchase: List[ResourceTypeEnum] = [ResourceTypeEnum.stone, ResourceTypeEnum.veg, ResourceTypeEnum.cow]
        
    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_hashcode_should_be_expected(self) -> None:
        self.assertEqual(self._result.hashcode, (((7 * 11) + 10) * 11) + 5)

    def test_then_result_items_to_purchase_should_contain_expected_number_of_items(self) -> None:
        self.assertEqual(len(self._result.items_to_purchase), 3)

    def test_then_result_items_to_purchase_should_be_expected(self) -> None:
        self.assertListEqual(self._result.items_to_purchase, self._expected_items_to_purchase)
