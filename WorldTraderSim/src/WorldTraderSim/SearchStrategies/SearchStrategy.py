#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Union
from DataTypes import Action, Country, Heuristic, Solution

DEFAULT_DEPTH_BOUND = 10
DEFAULT_MAX_FRONTIER_SIZE = 100

class SearchStrategy(object):

   DEPTH_BOUND: int
   MAX_FRONTIER_SIZE: int
   TREE_BASED_SEARCH: bool

   def __init__(self, tree_based_search: bool, depth_bound: int = DEFAULT_DEPTH_BOUND, frontier_size: int = DEFAULT_MAX_FRONTIER_SIZE) -> None:
      super().__init__()
      self.TREE_BASED_SEARCH = tree_based_search
      self.DEPTH_BOUND = depth_bound
      self.MAX_FRONTIER_SIZE = frontier_size

   def search(self, initial_state: List[Country], actions: List[Action], heuristic: Union[Heuristic, None]) -> Solution:
      raise NotImplementedError('ERROR: This method must be overridden by a concrete search strategy implementation')
