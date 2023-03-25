#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum
from typing import Callable, List
from .Country import Country

class ActionType(Enum):
  TRANSFER=1
  TRANSFORM=2

class Action(object):
  ACTION_TYPE: ActionType
  NEXT_STATE: Callable[[List[Country]], List[Country]]
  ACTION_COST: float
  PRECONDITIONS: List[Callable[[List[Country]], bool]]

  def __init__(self, preconditions: List[Callable[[List[Country]], bool]], cost: float, next_state_fn: Callable[[List[Country]], List[Country]]) -> None:
    super().__init__()
    self.NEXT_STATE = next_state_fn
    self.ACTION_COST = cost
    self.PRECONDITIONS = preconditions

  def apply(self, countries: List[Country]) -> List[Country]:
    return self.NEXT_STATE(countries) if all([precondition(countries) for precondition in self.PRECONDITIONS]) else None

  def calculate_action_cost(countries: List[Country]) -> float:
    return 0.0

  def get_impacted_countries(self) -> List[Country]:
    raise Exception("Not Implemented")

  def to_string(self, self_country: Country) -> str:
    raise Exception("Not Implemented")
