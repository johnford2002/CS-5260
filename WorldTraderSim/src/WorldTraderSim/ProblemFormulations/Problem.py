#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, List, Optional, Union
from DataTypes import Action, Country, Heuristic, Solution
from SearchStrategies import SearchStrategy

class Problem(object):

   STATES: Dict[str, Country]
   ACTIONS: List[Action]
   HEURISTIC: Union[Heuristic, None]

   def __init__(self, initial_state: Dict[str, Country], actions: List[Action], heuristic: Optional[Heuristic] = None) -> None:
      super().__init__()
      self.STATES = initial_state
      self.ACTIONS = actions
      self.HEURISTIC = heuristic

   def search(self, initial_state: Dict[str, Country], strategy: SearchStrategy) -> Solution:
      return strategy.search(initial_state, self.ACTIONS, self.HEURISTIC)
