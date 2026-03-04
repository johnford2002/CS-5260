import copy

from DataTypes import Country, ResourceQuantity, TransferAction
from DataTypes.TransferAction import TransferDirection


class TestTransferActionCreation:
    def test_creates_send_action(self, atlantis, europa):
        rq = ResourceQuantity("MetallicElements", 5)
        action = TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.SEND,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )
        assert action.DIRECTION == TransferDirection.SEND
        assert action.SENDER.name == "Atlantis"
        assert action.RECEIVER.name == "Europa"

    def test_creates_receive_action(self, atlantis, europa):
        rq = ResourceQuantity("MetallicElements", 5)
        action = TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.RECEIVE,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )
        assert action.DIRECTION == TransferDirection.RECEIVE
        assert action.SENDER.name == "Europa"
        assert action.RECEIVER.name == "Atlantis"

    def test_resource_quantities_stored(self, atlantis, europa):
        rq = ResourceQuantity("Timber", 3)
        action = TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.SEND,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )
        assert action.RESOURCE_QUANTITIES[0].name == "Timber"
        assert action.RESOURCE_QUANTITIES[0].quantity == 3


class TestTransferActionApply:
    def _send_action(self, atlantis, europa, resource_name, quantity):
        rq = ResourceQuantity(resource_name, quantity)
        return TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.SEND,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )

    def test_send_reduces_sender_resource(self, atlantis, europa, country_states):
        action = self._send_action(atlantis, europa, "MetallicElements", 10)
        new_states = action.apply(copy.deepcopy(country_states))
        assert new_states["Atlantis"].resources["MetallicElements"].quantity == 90

    def test_send_increases_receiver_resource(self, atlantis, europa, country_states):
        action = self._send_action(atlantis, europa, "MetallicElements", 10)
        new_states = action.apply(copy.deepcopy(country_states))
        assert new_states["Europa"].resources["MetallicElements"].quantity == 60

    def test_apply_returns_none_when_precondition_fails(self, atlantis, europa, country_states):
        # Atlantis has 0 MetallicAlloys — send of 1 should fail
        action = self._send_action(atlantis, europa, "MetallicAlloys", 1)
        result = action.apply(copy.deepcopy(country_states))
        assert result is None

    def test_original_states_not_mutated(self, atlantis, europa, country_states):
        action = self._send_action(atlantis, europa, "MetallicElements", 10)
        original_qty = atlantis.resources["MetallicElements"].quantity
        action.apply(copy.deepcopy(country_states))
        assert atlantis.resources["MetallicElements"].quantity == original_qty


class TestTransferActionToString:
    def test_send_format(self, atlantis, europa):
        rq = ResourceQuantity("Housing", 3)
        action = TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.SEND,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )
        result = action.to_string(atlantis)
        assert "self" in result
        assert "Europa" in result
        assert "Housing 3" in result

    def test_receive_format(self, atlantis, europa):
        rq = ResourceQuantity("Timber", 2)
        action = TransferAction.create_from_resource_quantities(
            resource_quantities=[rq],
            transfer_direction=TransferDirection.RECEIVE,
            self_country=atlantis,
            other_country=europa,
            cost_fn=lambda _: 0.0,
        )
        result = action.to_string(atlantis)
        assert "self" in result
        assert "Europa" in result
