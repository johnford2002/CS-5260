#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Libraries
from __future__ import annotations
from typing import Dict
from uuid import UUID, uuid4

# Local Modules
from .Action import Action
from .Country import Country

class Node(object):

   ID: UUID
   STATE: Dict[str, Country]
   PARENT: Node
   PARENT_ACTION: Action
   PATH_COST: float

   def __init__(self, state: Dict[str, Country], parent: Node, parent_action: Action, path_cost: float) -> None:
      super().__init__()
      self.ID = uuid4()
      self.STATE = state
      self.PARENT = parent
      self.PARENT_ACTION = parent_action
      self.PATH_COST = path_cost

   def __eq__(self, other: Node) -> bool:
      return self.ID == other.ID

   def __hash__(self) -> int:
      return hash(self.ID)

   def depth(self):
      node_count = 1
      current_node = self.PARENT
      while current_node:
         node_count += 1
         current_node = current_node.PARENT
      return node_count
