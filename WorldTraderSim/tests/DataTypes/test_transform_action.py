import copy

from DataTypes import Country, ResourceQuantity, TransformAction, TransformTemplate


def _single_input_template():
    """Simple template: 2 MetallicElements -> 1 MetallicAlloys + 1 waste."""
    return TransformTemplate(
        name="simple_alloys",
        inputs=[ResourceQuantity("MetallicElements", 2)],
        outputs=[
            ResourceQuantity("MetallicAlloys", 1),
            ResourceQuantity("MetallicAlloysWaste", 1),
        ],
    )


class TestTransformActionCreation:
    def test_creates_one_action_per_multiplier(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=1,
        )
        assert len(actions) == 1

    def test_creates_multiple_actions_for_quantity_max(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=3,
        )
        assert len(actions) == 3

    def test_action_has_correct_template_name(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=1,
        )
        assert actions[0].TEMPLATE.name == "alloys"

    def test_target_country_set(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=1,
        )
        assert actions[0].TARGET.name == "Atlantis"


class TestTransformActionApply:
    def test_apply_produces_outputs(self, atlantis, country_states):
        template = _single_input_template()
        actions = TransformAction.create_from_transform_template(
            transform_template=template,
            target_country=atlantis,
            quantity_max=1,
        )
        new_states = actions[0].apply(copy.deepcopy(country_states))
        assert new_states["Atlantis"].resources["MetallicAlloys"].quantity == 1

    def test_apply_consumes_inputs(self, atlantis, country_states):
        template = _single_input_template()
        actions = TransformAction.create_from_transform_template(
            transform_template=template,
            target_country=atlantis,
            quantity_max=1,
        )
        new_states = actions[0].apply(copy.deepcopy(country_states))
        assert new_states["Atlantis"].resources["MetallicElements"].quantity == 98

    def test_apply_returns_none_when_insufficient_resources(self, atlantis, country_states):
        # MetallicAlloys starts at 0; require 5 of them
        template = TransformTemplate(
            name="impossible",
            inputs=[ResourceQuantity("MetallicAlloys", 5)],
            outputs=[ResourceQuantity("Housing", 1)],
        )
        actions = TransformAction.create_from_transform_template(
            transform_template=template,
            target_country=atlantis,
            quantity_max=1,
        )
        result = actions[0].apply(copy.deepcopy(country_states))
        assert result is None

    def test_apply_does_not_mutate_original_state(self, atlantis, country_states):
        template = _single_input_template()
        actions = TransformAction.create_from_transform_template(
            transform_template=template,
            target_country=atlantis,
            quantity_max=1,
        )
        original_qty = atlantis.resources["MetallicElements"].quantity
        actions[0].apply(copy.deepcopy(country_states))
        assert atlantis.resources["MetallicElements"].quantity == original_qty


class TestTransformActionToString:
    def test_includes_transform_keyword(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=1,
        )
        result = actions[0].to_string(atlantis)
        assert "TRANSFORM" in result

    def test_self_country_shown_as_self(self, atlantis, alloys_template):
        actions = TransformAction.create_from_transform_template(
            transform_template=alloys_template,
            target_country=atlantis,
            quantity_max=1,
        )
        result = actions[0].to_string(atlantis)
        assert "self" in result
