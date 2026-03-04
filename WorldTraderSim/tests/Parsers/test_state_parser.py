import io
import os
import tempfile

import pytest

import Parsers.StateParser as StateParser


REQUIRED_NAMES = [
    "Population",
    "MetallicElements",
    "Timber",
    "MetallicAlloys",
    "MetallicAlloysWaste",
    "Electronics",
    "ElectronicsWaste",
    "Housing",
    "HousingWaste",
]


class TestValidateResources:
    def test_returns_true_for_complete_list(self):
        assert StateParser.validate_resources(REQUIRED_NAMES) is True

    def test_returns_false_when_resource_missing(self):
        incomplete = [r for r in REQUIRED_NAMES if r != "Housing"]
        assert StateParser.validate_resources(incomplete) is False

    def test_returns_false_for_empty_list(self):
        assert StateParser.validate_resources([]) is False

    def test_extra_resources_are_allowed(self):
        extended = REQUIRED_NAMES + ["Housing2", "Housing3"]
        assert StateParser.validate_resources(extended) is True


class TestValidateInitialState:
    def _make_row(self, country_name="TestCountry"):
        row = {"Country": country_name}
        for name in REQUIRED_NAMES:
            row[name] = "100"
        return row

    def test_returns_true_for_valid_state(self):
        state = [self._make_row("Atlantis"), self._make_row("Europa")]
        assert StateParser.validate_initial_state(state) is True

    def test_returns_false_when_country_missing_resource(self):
        row = self._make_row("Atlantis")
        del row["Housing"]
        assert StateParser.validate_initial_state([row]) is False

    def test_single_valid_country(self):
        state = [self._make_row("Solo")]
        assert StateParser.validate_initial_state(state) is True


class TestReadCsv:
    def test_reads_rows_as_dicts(self):
        csv_content = "Country,Population\nAtlantis,100\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            tmp_path = f.name
        try:
            result = StateParser.read_csv(tmp_path)
            assert len(result) == 1
            assert result[0]["Country"] == "Atlantis"
            assert result[0]["Population"] == "100"
        finally:
            os.unlink(tmp_path)

    def test_reads_multiple_rows(self):
        csv_content = "Country,Population\nAtlantis,100\nEuropa,80\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            tmp_path = f.name
        try:
            result = StateParser.read_csv(tmp_path)
            assert len(result) == 2
        finally:
            os.unlink(tmp_path)

    def test_reads_actual_balanced_initial_state(self):
        states_dir = os.path.join(
            os.path.dirname(__file__), "..", "..",
            "src", "WorldTraderSim", "data", "states",
        )
        path = os.path.join(states_dir, "initial-balanced.csv")
        result = StateParser.read_csv(path)
        assert len(result) == 5
        assert result[0]["Country"] == "Atlantis"
