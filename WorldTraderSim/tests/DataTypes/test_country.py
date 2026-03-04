import copy

from DataTypes import Country, ResourceQuantity


class TestCountryFromDict:
    def test_sets_name(self):
        data = {"Country": "Atlantis", "Population": "100"}
        country = Country.from_dict(data)
        assert country.name == "Atlantis"

    def test_creates_resource_quantities_with_correct_values(self):
        data = {"Country": "Atlantis", "Population": "100", "MetallicElements": "50"}
        country = Country.from_dict(data)
        assert country.resources["Population"].quantity == 100
        assert country.resources["MetallicElements"].quantity == 50

    def test_resource_names_match_column_headers(self):
        data = {"Country": "Atlantis", "Housing": "3"}
        country = Country.from_dict(data)
        assert "Housing" in country.resources

    def test_country_key_not_in_resources(self):
        data = {"Country": "Atlantis", "Population": "10"}
        country = Country.from_dict(data)
        assert "Country" not in country.resources


class TestCountryHasResourceQuantity:
    def test_returns_true_when_exactly_enough(self, atlantis):
        assert atlantis.has_resource_quantity("Population", 100) is True

    def test_returns_true_when_more_than_enough(self, atlantis):
        assert atlantis.has_resource_quantity("Population", 50) is True

    def test_returns_false_when_insufficient(self, atlantis):
        assert atlantis.has_resource_quantity("Population", 101) is False

    def test_zero_required_always_satisfied(self, atlantis):
        assert atlantis.has_resource_quantity("MetallicAlloys", 0) is True

    def test_resource_at_zero_fails_positive_requirement(self, atlantis):
        assert atlantis.has_resource_quantity("MetallicAlloys", 1) is False


class TestCountryDiffResourceQuantities:
    def test_detects_increase(self):
        start = Country(name="A", resources={"Housing": ResourceQuantity("Housing", 0)})
        end = Country(name="A", resources={"Housing": ResourceQuantity("Housing", 3)})
        diffs = Country.diff_resource_quantities(start, end)
        assert len(diffs) == 1
        assert diffs[0].name == "Housing"
        assert diffs[0].quantity == 3

    def test_detects_decrease(self):
        start = Country(name="A", resources={"MetallicElements": ResourceQuantity("MetallicElements", 100)})
        end = Country(name="A", resources={"MetallicElements": ResourceQuantity("MetallicElements", 98)})
        diffs = Country.diff_resource_quantities(start, end)
        assert len(diffs) == 1
        assert diffs[0].quantity == -2

    def test_no_change_returns_empty_list(self):
        country = Country(name="A", resources={"Housing": ResourceQuantity("Housing", 5)})
        same = copy.deepcopy(country)
        diffs = Country.diff_resource_quantities(country, same)
        assert diffs == []

    def test_only_changed_resources_appear(self, atlantis):
        end = copy.deepcopy(atlantis)
        end.resources["Housing"].quantity = 5
        diffs = Country.diff_resource_quantities(atlantis, end)
        names = [d.name for d in diffs]
        assert names == ["Housing"]
