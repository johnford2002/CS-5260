#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .SearchStrategy import SearchStrategy
from .GreedyBestFirstSearch import GreedyBestFirstSearch
from .HeuristicDepthFirstSearch import HeuristicDepthFirstSearch

def search_strategy_factory(search_strategy_class_name: str) -> SearchStrategy:
    if search_strategy_class_name == "GreedyBestFirstSearch":
        return GreedyBestFirstSearch
    if search_strategy_class_name == "HeuristicDepthFirstSearch":
        return HeuristicDepthFirstSearch
    else:
        raise Exception("Unrecognized Search Strategy Class '{}'".format(search_strategy_class_name))
