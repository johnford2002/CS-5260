from DataTypes import ResourceQuantity


class TestResourceQuantity:
    def test_stores_name_and_quantity(self):
        rq = ResourceQuantity("Housing", 5)
        assert rq.name == "Housing"
        assert rq.quantity == 5

    def test_str_format(self):
        rq = ResourceQuantity("Timber", 10)
        assert str(rq) == "Timber 10"

    def test_iter_yields_name_and_quantity_keys(self):
        rq = ResourceQuantity("Population", 42)
        d = dict(rq)
        assert d == {"name": "Population", "quantity": 42}

    def test_zero_quantity(self):
        rq = ResourceQuantity("MetallicAlloys", 0)
        assert rq.quantity == 0
        assert str(rq) == "MetallicAlloys 0"
