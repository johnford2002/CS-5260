#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .SearchStrategy import SearchStrategy
from .BestFirstSearch import BestFirstSearch
from .HeuristicDepthFirstSearch import HeuristicDepthFirstSearch

def search_strategy_factory(search_strategy_class_name: str) -> SearchStrategy:
    if search_strategy_class_name == "BestFirstSearch":
        return BestFirstSearch
    if search_strategy_class_name == "HeuristicDepthFirstSearch":
        return HeuristicDepthFirstSearch
    else:
        raise Exception("Unrecognized Search Strategy Class '{}'".format(search_strategy_class_name))
