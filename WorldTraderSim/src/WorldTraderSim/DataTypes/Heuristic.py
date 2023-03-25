#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Callable
from .Node import Node

class Heuristic(object):

   EVALUATION: Callable[[Node], float]

   def __init__(self, evaluation_function: Callable[[Node], float]) -> None:
      super().__init__()
      self.EVALUATION = evaluation_function

   def apply(self, node: Node) -> float:
      return self.EVALUATION(node)
