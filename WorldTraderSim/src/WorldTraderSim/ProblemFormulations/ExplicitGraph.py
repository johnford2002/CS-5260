#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, List, Optional
from DataTypes import Action, Country, Heuristic
from .Problem import Problem

class ExplicitGraph(Problem):

   def __init__(self, initial_state: Dict[str,Country], actions: List[Action], heuristic: Optional[Heuristic] = None) -> None:
      super().__init__(initial_state, actions, heuristic)
