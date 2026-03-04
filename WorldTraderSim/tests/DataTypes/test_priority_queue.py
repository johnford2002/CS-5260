import copy

from DataTypes import Node, PriorityQueue, ResourceQuantity, Country


def make_node(path_cost, atlantis):
    """Create a minimal Node with a unique state to avoid hash collisions."""
    state = {
        "Atlantis": Country(
            name="Atlantis",
            resources={"Housing": ResourceQuantity("Housing", int(path_cost * 100))},
        )
    }
    node = Node(state=state, parent=None, parent_action=None, path_cost=path_cost)
    return node


class TestPriorityQueueAscending:
    """ascending=True uses operator.gt — higher costs are inserted earlier.
    pop() removes from the end, so returns the lowest-cost item first."""

    def test_is_empty_on_creation(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=True)
        assert pq.is_empty() is True

    def test_not_empty_after_add(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=True)
        pq.add(make_node(1.0, atlantis))
        assert pq.is_empty() is False

    def test_length_tracks_additions(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=True)
        pq.add(make_node(1.0, atlantis))
        pq.add(make_node(2.0, atlantis))
        assert pq.length() == 2

    def test_pop_returns_lowest_cost_node(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=True)
        low = make_node(1.0, atlantis)
        high = make_node(5.0, atlantis)
        mid = make_node(3.0, atlantis)
        pq.add(high)
        pq.add(low)
        pq.add(mid)
        popped = pq.pop()
        assert popped.PATH_COST == 1.0

    def test_as_list_returns_ascending_order(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=True)
        pq.add(make_node(3.0, atlantis))
        pq.add(make_node(1.0, atlantis))
        pq.add(make_node(2.0, atlantis))
        costs = [n.PATH_COST for n in pq.as_list()]
        assert costs == sorted(costs)


class TestPriorityQueueDescending:
    """ascending=False uses operator.lt — lower costs are inserted earlier.
    pop() returns the highest-cost item."""

    def test_pop_returns_highest_cost_node(self, atlantis):
        pq = PriorityQueue(eval_fn=lambda n: n.PATH_COST, ascending=False)
        low = make_node(1.0, atlantis)
        high = make_node(5.0, atlantis)
        pq.add(low)
        pq.add(high)
        popped = pq.pop()
        assert popped.PATH_COST == 5.0
