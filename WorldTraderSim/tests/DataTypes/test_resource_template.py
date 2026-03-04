from DataTypes import ResourceTemplate


class TestResourceTemplateFromDict:
    def test_creates_name_weight_factor(self):
        data = {"Resource": "Housing", "Weight": "0.9", "Factor": ""}
        rt = ResourceTemplate.from_dict(data)
        assert rt.name == "Housing"
        assert rt.weight == 0.9
        assert rt.factor == ""

    def test_negative_weight(self):
        data = {"Resource": "HousingWaste", "Weight": "-0.15", "Factor": ""}
        rt = ResourceTemplate.from_dict(data)
        assert rt.weight == -0.15


class TestResourceTemplateTransferable:
    def test_population_is_not_transferable(self):
        rt = ResourceTemplate(name="Population", weight=0.3, factor="")
        assert rt.transferable() is False

    def test_other_resources_are_transferable(self):
        for name in ["Housing", "MetallicElements", "Timber", "Electronics"]:
            rt = ResourceTemplate(name=name, weight=0.1, factor="")
            assert rt.transferable() is True, f"{name} should be transferable"
