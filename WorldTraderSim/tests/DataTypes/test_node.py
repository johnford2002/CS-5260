import copy

from DataTypes import Country, Node, ResourceQuantity


def make_state(atlantis):
    return {"Atlantis": copy.deepcopy(atlantis)}


class TestNodeStateHash:
    def test_returns_string(self, atlantis):
        node = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        assert isinstance(node.state_hash(), str)

    def test_same_state_produces_same_hash(self, atlantis):
        state_a = make_state(atlantis)
        state_b = copy.deepcopy(state_a)
        node_a = Node(state=state_a, parent=None, parent_action=None, path_cost=0.0)
        node_b = Node(state=state_b, parent=None, parent_action=None, path_cost=0.0)
        assert node_a.state_hash() == node_b.state_hash()

    def test_different_state_produces_different_hash(self, atlantis):
        state_a = make_state(atlantis)
        state_b = copy.deepcopy(state_a)
        state_b["Atlantis"].resources["Housing"].quantity = 99
        node_a = Node(state=state_a, parent=None, parent_action=None, path_cost=0.0)
        node_b = Node(state=state_b, parent=None, parent_action=None, path_cost=0.0)
        assert node_a.state_hash() != node_b.state_hash()

    def test_hash_is_cached_after_first_call(self, atlantis):
        node = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        first = node.state_hash()
        # Mutate internal state after first hash to confirm cache is used
        node.STATE["Atlantis"].resources["Housing"].quantity = 999
        second = node.state_hash()
        assert first == second


class TestNodeDepth:
    def test_root_node_has_depth_1(self, atlantis):
        node = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        assert node.depth() == 1

    def test_child_node_has_depth_2(self, atlantis):
        root = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        child_state = copy.deepcopy(make_state(atlantis))
        child = Node(state=child_state, parent=root, parent_action=None, path_cost=0.0)
        assert child.depth() == 2

    def test_grandchild_node_has_depth_3(self, atlantis):
        root = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        child = Node(state=copy.deepcopy(make_state(atlantis)), parent=root, parent_action=None, path_cost=0.0)
        grandchild = Node(state=copy.deepcopy(make_state(atlantis)), parent=child, parent_action=None, path_cost=0.0)
        assert grandchild.depth() == 3

    def test_depth_is_cached(self, atlantis):
        node = Node(state=make_state(atlantis), parent=None, parent_action=None, path_cost=0.0)
        first = node.depth()
        node.PARENT = node  # corrupt — should not recompute
        second = node.depth()
        assert first == second


class TestNodeEquality:
    def test_equal_nodes_have_same_hash(self, atlantis):
        state_a = make_state(atlantis)
        state_b = copy.deepcopy(state_a)
        node_a = Node(state=state_a, parent=None, parent_action=None, path_cost=0.0)
        node_b = Node(state=state_b, parent=None, parent_action=None, path_cost=0.0)
        assert node_a == node_b

    def test_unequal_states_are_not_equal(self, atlantis):
        state_a = make_state(atlantis)
        state_b = copy.deepcopy(state_a)
        state_b["Atlantis"].resources["Housing"].quantity = 5
        node_a = Node(state=state_a, parent=None, parent_action=None, path_cost=0.0)
        node_b = Node(state=state_b, parent=None, parent_action=None, path_cost=0.0)
        assert node_a != node_b
