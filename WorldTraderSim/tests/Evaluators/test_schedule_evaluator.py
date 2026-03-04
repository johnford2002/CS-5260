"""
Tests for ScheduleEvaluator.

Schedule and Node objects are constructed minimally: a root Node (PARENT=None,
PARENT_ACTION=None) means depth()=1 and get_impacted_countries()=[], which
simplifies the math while still exercising the evaluator's core logic.
"""
import copy
import configparser

import pytest

from DataTypes import Country, Node, ResourceQuantity, ResourceTemplate, Schedule
from Evaluators.StateEvaluator import StateEvaluator
from Evaluators.ScheduleEvaluator import ScheduleEvaluator


def _make_country(name, housing=0, population=100):
    return Country(
        name=name,
        resources={
            "Population": ResourceQuantity("Population", population),
            "MetallicElements": ResourceQuantity("MetallicElements", 0),
            "Timber": ResourceQuantity("Timber", 0),
            "MetallicAlloys": ResourceQuantity("MetallicAlloys", 0),
            "MetallicAlloysWaste": ResourceQuantity("MetallicAlloysWaste", 0),
            "Electronics": ResourceQuantity("Electronics", 0),
            "ElectronicsWaste": ResourceQuantity("ElectronicsWaste", 0),
            "Housing": ResourceQuantity("Housing", housing),
            "HousingWaste": ResourceQuantity("HousingWaste", 0),
        },
    )


def _make_schedule(state_dict):
    """Wrap a state dict in a root Node and a Schedule."""
    node = Node(state=state_dict, parent=None, parent_action=None, path_cost=0.0)
    return Schedule(node=node)


@pytest.fixture
def resources():
    return [
        ResourceTemplate(name="Population", weight=0.3, factor=""),
        ResourceTemplate(name="MetallicElements", weight=0.025, factor=""),
        ResourceTemplate(name="Timber", weight=0.015, factor=""),
        ResourceTemplate(name="MetallicAlloys", weight=0.2, factor=""),
        ResourceTemplate(name="MetallicAlloysWaste", weight=-0.1, factor=""),
        ResourceTemplate(name="Electronics", weight=0.35, factor=""),
        ResourceTemplate(name="ElectronicsWaste", weight=-0.2, factor=""),
        ResourceTemplate(name="Housing", weight=0.9, factor=""),
        ResourceTemplate(name="HousingWaste", weight=-0.15, factor=""),
    ]


@pytest.fixture
def state_evaluator(resources):
    return StateEvaluator(resources)


@pytest.fixture
def start_country():
    return _make_country("Atlantis", housing=0)


@pytest.fixture
def evaluator(start_country, state_evaluator):
    initial = {"Atlantis": copy.deepcopy(start_country)}
    return ScheduleEvaluator(
        initial_state=initial,
        state_quality_fn=state_evaluator.state_quality,
        self_country_name="Atlantis",
    )


class TestLogisticFunction:
    def test_at_midpoint_returns_half(self, evaluator):
        # Default midpoint is 0; logistic(0) = 0.5
        assert evaluator.logistic_function(0) == pytest.approx(0.5)

    def test_large_positive_approaches_one(self, evaluator):
        result = evaluator.logistic_function(1000)
        assert result > 0.999

    def test_large_negative_approaches_zero(self, evaluator):
        result = evaluator.logistic_function(-1000)
        assert result < 0.001

    def test_positive_x_above_half(self, evaluator):
        assert evaluator.logistic_function(1) > 0.5

    def test_negative_x_below_half(self, evaluator):
        assert evaluator.logistic_function(-1) < 0.5


class TestDiscountedReward:
    def test_no_change_yields_zero(self, evaluator, start_country):
        schedule = _make_schedule({"Atlantis": copy.deepcopy(start_country)})
        result = evaluator.discounted_reward(start_country, schedule)
        assert result == pytest.approx(0.0)

    def test_improvement_yields_positive_reward(self, evaluator, start_country):
        improved = copy.deepcopy(start_country)
        improved.resources["Housing"].quantity = 5  # +4.5 state quality
        schedule = _make_schedule({"Atlantis": improved})
        result = evaluator.discounted_reward(start_country, schedule)
        assert result > 0

    def test_degradation_yields_negative_reward(self, evaluator, start_country):
        worse = copy.deepcopy(start_country)
        worse.resources["HousingWaste"].quantity = 10  # negative weight
        schedule = _make_schedule({"Atlantis": worse})
        result = evaluator.discounted_reward(start_country, schedule)
        assert result < 0

    def test_discount_applied_by_depth(self, evaluator, start_country):
        improved = copy.deepcopy(start_country)
        improved.resources["Housing"].quantity = 5
        schedule = _make_schedule({"Atlantis": improved})
        # depth() == 1, discount == 0.999^1
        undiscounted = evaluator.undiscounted_reward(start_country, schedule)
        discounted = evaluator.discounted_reward(start_country, schedule)
        assert discounted == pytest.approx(undiscounted * (0.999 ** 1))


class TestExpectedUtility:
    def test_no_change_returns_zero(self, evaluator, start_country):
        """Root node has no PARENT_ACTION so get_impacted_countries() is empty.
        schedule_success_probability returns 1 (empty product), failure_probability=0.
        EU = 1*0 + 0*(-0.35) = 0.0."""
        schedule = _make_schedule({"Atlantis": copy.deepcopy(start_country)})
        result = evaluator.expected_utility(start_country, schedule)
        assert result == pytest.approx(0.0)

    def test_improvement_gives_higher_eu_than_no_change(self, evaluator, start_country):
        no_change_schedule = _make_schedule({"Atlantis": copy.deepcopy(start_country)})
        improved = copy.deepcopy(start_country)
        improved.resources["Housing"].quantity = 10
        improved_schedule = _make_schedule({"Atlantis": improved})

        eu_no_change = evaluator.expected_utility(start_country, no_change_schedule)
        eu_improved = evaluator.expected_utility(start_country, improved_schedule)
        assert eu_improved > eu_no_change


class TestConfigure:
    def test_configure_overrides_failed_impact(self, start_country, state_evaluator):
        initial = {"Atlantis": copy.deepcopy(start_country)}
        ev = ScheduleEvaluator(
            initial_state=initial,
            state_quality_fn=state_evaluator.state_quality,
            self_country_name="Atlantis",
        )
        config = configparser.ConfigParser()
        config.read_dict({"ScheduleEvaluation": {"FailedImpact": "-0.5"}})
        ev.configure(config)
        assert ev.schedule_failed_impact == pytest.approx(-0.5)

    def test_configure_overrides_length_impact(self, start_country, state_evaluator):
        initial = {"Atlantis": copy.deepcopy(start_country)}
        ev = ScheduleEvaluator(
            initial_state=initial,
            state_quality_fn=state_evaluator.state_quality,
            self_country_name="Atlantis",
        )
        config = configparser.ConfigParser()
        config.read_dict({"ScheduleEvaluation": {"LengthImpact": "0.95"}})
        ev.configure(config)
        assert ev.schedule_length_impact == pytest.approx(0.95)

    def test_configure_with_empty_config_keeps_defaults(self, start_country, state_evaluator):
        initial = {"Atlantis": copy.deepcopy(start_country)}
        ev = ScheduleEvaluator(
            initial_state=initial,
            state_quality_fn=state_evaluator.state_quality,
            self_country_name="Atlantis",
        )
        ev.configure(configparser.ConfigParser())
        assert ev.schedule_failed_impact == pytest.approx(-0.35)
        assert ev.schedule_length_impact == pytest.approx(0.999)
