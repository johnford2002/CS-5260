import os
import tempfile

import pytest

import Parsers.TransformTemplateParser as TemplateParser


VALID_TEMPLATE = """(TRANSFORM alloys
  (INPUTS (Population 1)
          (MetallicElements 2))
  (OUTPUTS (Population 1)
           (MetallicAlloys 1)
           (MetallicAlloysWaste 1)))
"""


class TestValidateNonempty:
    def test_empty_string_is_invalid(self):
        assert TemplateParser.validate_nonempty("") is False

    def test_nonempty_string_is_valid(self):
        assert TemplateParser.validate_nonempty("(TRANSFORM x (INPUTS) (OUTPUTS))") is True


class TestValidateEnclosed:
    def test_balanced_parens_valid(self):
        assert TemplateParser.validate_enclosed("(hello (world))") is True

    def test_unbalanced_open_paren_invalid(self):
        assert TemplateParser.validate_enclosed("(hello (world)") is False

    def test_unbalanced_close_paren_invalid(self):
        assert TemplateParser.validate_enclosed("hello world))") is False

    def test_no_parens_valid(self):
        assert TemplateParser.validate_enclosed("no parens here") is True


class TestValidateKeywords:
    def test_all_keywords_present(self):
        assert TemplateParser.validate_keywords(VALID_TEMPLATE) is True

    def test_missing_transform_keyword_invalid(self):
        bad = VALID_TEMPLATE.replace("TRANSFORM", "XFORM")
        assert TemplateParser.validate_keywords(bad) is False

    def test_missing_inputs_keyword_invalid(self):
        bad = VALID_TEMPLATE.replace("INPUTS", "IN")
        assert TemplateParser.validate_keywords(bad) is False

    def test_missing_outputs_keyword_invalid(self):
        bad = VALID_TEMPLATE.replace("OUTPUTS", "OUT")
        assert TemplateParser.validate_keywords(bad) is False


class TestValidate:
    def test_valid_template_does_not_raise(self):
        TemplateParser.validate(VALID_TEMPLATE)  # no exception

    def test_empty_template_raises(self):
        with pytest.raises(Exception, match="Empty"):
            TemplateParser.validate("")

    def test_unbalanced_parens_raises(self):
        with pytest.raises(Exception):
            TemplateParser.validate("(TRANSFORM (INPUTS (OUTPUTS)")

    def test_missing_keyword_raises(self):
        with pytest.raises(Exception):
            TemplateParser.validate("(XFORM (IN (OUT))")


class TestBuildResourceQuantities:
    def test_parses_single_resource(self):
        block = "(INPUTS (MetallicElements 2))"
        quantities = TemplateParser.build_resource_quantities(block)
        assert len(quantities) == 1
        assert quantities[0].name == "MetallicElements"
        assert quantities[0].quantity == 2

    def test_parses_multiple_resources(self):
        block = "(INPUTS (Population 1) (MetallicElements 2))"
        quantities = TemplateParser.build_resource_quantities(block)
        assert len(quantities) == 2

    def test_empty_block_returns_empty_list(self):
        quantities = TemplateParser.build_resource_quantities("(INPUTS)")
        assert quantities == []


class TestParse:
    def test_parse_actual_alloys_template(self):
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "..",
            "src", "WorldTraderSim", "data", "templates", "base", "alloys.tmpl",
        )
        template = TemplateParser.parse(template_path)
        assert template.name == "alloys"
        assert len(template.inputs) == 2
        assert len(template.outputs) == 3

    def test_parse_uses_filename_as_name(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tmpl", prefix="mytemplate_", delete=False
        ) as f:
            f.write(VALID_TEMPLATE)
            tmp_path = f.name
        try:
            template = TemplateParser.parse(tmp_path)
            # Name comes from filename without extension
            assert template.name == os.path.splitext(os.path.basename(tmp_path))[0]
        finally:
            os.unlink(tmp_path)

    def test_parse_input_quantities(self):
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "..",
            "src", "WorldTraderSim", "data", "templates", "base", "alloys.tmpl",
        )
        template = TemplateParser.parse(template_path)
        input_names = [rq.name for rq in template.inputs]
        assert "Population" in input_names
        assert "MetallicElements" in input_names
