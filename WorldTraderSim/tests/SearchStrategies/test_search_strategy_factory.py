import pytest

from SearchStrategies import search_strategy_factory, HeuristicDepthFirstSearch, BestFirstSearch


class TestSearchStrategyFactory:
    def test_returns_heuristic_dfs_class(self):
        cls = search_strategy_factory("HeuristicDepthFirstSearch")
        assert cls is HeuristicDepthFirstSearch

    def test_returns_best_first_search_class(self):
        cls = search_strategy_factory("BestFirstSearch")
        assert cls is BestFirstSearch

    def test_raises_for_unknown_strategy(self):
        with pytest.raises(Exception, match="Unrecognized"):
            search_strategy_factory("NonExistentStrategy")

    def test_returned_class_is_instantiable(self):
        cls = search_strategy_factory("HeuristicDepthFirstSearch")
        # tree_based_search=True, depth_bound=10, frontier_size=100
        instance = cls(True, 10, 100)
        assert instance.DEPTH_BOUND == 10
        assert instance.MAX_FRONTIER_SIZE == 100
        assert instance.TREE_BASED_SEARCH is True
