#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import logging
from typing import Dict, List, Union

from DataTypes import Action, Country, Heuristic, Node, PriorityQueue, Solution
from .SearchStrategy import SearchStrategy

class BestFirstSearch(SearchStrategy):
   def _expand(self, actions: List[Action], heuristic: Heuristic, node: Node) -> List[Node]:
      nodes = PriorityQueue(lambda node: heuristic.apply(node), False)
      for action in actions:
         next_state = action.apply(node.STATE)
         if next_state is not None:
            logging.debug(node.STATE)
            logging.debug(action.ACTION_TYPE)
            nodes.add(Node(next_state, node, action, node.PATH_COST + action.ACTION_COST))
      return nodes.as_list()

   def search_with_reached(self, country_states: Dict[str, Country], actions: List[Action], heuristic: Union[Heuristic, None]) -> Solution:
      visited = []
      node = Node(country_states, None, None, 0.0)
      frontier = PriorityQueue(lambda node: heuristic.apply(node), True).add(node)
      reached = { node.state_hash(): node }
      while not frontier.is_empty():
         node = frontier.pop()
         visited.append(node.STATE)
         if node.depth() >= self.DEPTH_BOUND:
            return Solution(node, visited)
         for child in self._expand(actions, heuristic, node):
            child_state_hash = child.state_hash()
            if child_state_hash not in reached or child.PATH_COST < reached[child_state_hash].PATH_COST:
               reached[child_state_hash] = child
               if frontier.length() < self.MAX_FRONTIER_SIZE:
                  frontier.add(child)
      return Solution(None)

   def search_without_reached(self, country_states: Dict[str, Country], actions: List[Action], heuristic: Union[Heuristic, None]) -> Solution:
      visited = []
      node = Node(country_states, None, None, 0.0)
      frontier = PriorityQueue(lambda node: heuristic.apply(node), True).add(node)
      while not frontier.is_empty():
         node = frontier.pop()
         visited.append(node.STATE)
         if node.depth() >= self.DEPTH_BOUND:
            return Solution(node, visited)
         for child in self._expand(actions, heuristic, node):
            if frontier.length() < self.MAX_FRONTIER_SIZE:
               frontier.add(child)
      return Solution(None)

   def search(self, country_states: Dict[str, Country], actions: List[Action], heuristic: Union[Heuristic, None]) -> Solution:
      logging.info(f"Searching with frontier size {self.MAX_FRONTIER_SIZE}")
      search_function = self.search_without_reached if self.TREE_BASED_SEARCH else self.search_with_reached
      return search_function(country_states, actions, heuristic)
