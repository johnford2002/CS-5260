import pytest

from DataTypes import Country, ResourceQuantity, ResourceTemplate
from Evaluators.StateEvaluator import StateEvaluator


class TestStateEvaluatorWeightedSum:
    def test_zero_resources_returns_zero(self, basic_resources):
        evaluator = StateEvaluator(basic_resources)
        zero_country = Country(
            name="Empty",
            resources={r.name: ResourceQuantity(r.name, 0) for r in basic_resources},
        )
        assert evaluator.state_quality(zero_country) == 0.0

    def test_single_resource_positive_weight(self):
        resources = [ResourceTemplate(name="Housing", weight=0.9, factor="")]
        evaluator = StateEvaluator(resources)
        country = Country(
            name="Test",
            resources={"Housing": ResourceQuantity("Housing", 10)},
        )
        assert evaluator.state_quality(country) == pytest.approx(9.0)

    def test_negative_weight_reduces_score(self):
        resources = [ResourceTemplate(name="HousingWaste", weight=-0.15, factor="")]
        evaluator = StateEvaluator(resources)
        country = Country(
            name="Test",
            resources={"HousingWaste": ResourceQuantity("HousingWaste", 10)},
        )
        assert evaluator.state_quality(country) == pytest.approx(-1.5)

    def test_multiple_resources_summed(self, basic_resources):
        evaluator = StateEvaluator(basic_resources)
        country = Country(
            name="Test",
            resources={
                "Population": ResourceQuantity("Population", 100),      # 0.3 * 100 = 30
                "MetallicElements": ResourceQuantity("MetallicElements", 0),
                "Timber": ResourceQuantity("Timber", 0),
                "MetallicAlloys": ResourceQuantity("MetallicAlloys", 0),
                "MetallicAlloysWaste": ResourceQuantity("MetallicAlloysWaste", 0),
                "Electronics": ResourceQuantity("Electronics", 0),
                "ElectronicsWaste": ResourceQuantity("ElectronicsWaste", 0),
                "Housing": ResourceQuantity("Housing", 10),             # 0.9 * 10  = 9
                "HousingWaste": ResourceQuantity("HousingWaste", 0),
            },
        )
        assert evaluator.state_quality(country) == pytest.approx(39.0)

    def test_balanced_initial_state_score(self, basic_resources, atlantis):
        """Atlantis: Pop=100, MetalEl=100, Timber=50, rest=0 → 30 + 2.5 + 0.75 = 33.25"""
        evaluator = StateEvaluator(basic_resources)
        assert evaluator.state_quality(atlantis) == pytest.approx(33.25)
