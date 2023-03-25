#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Libraries
from __future__ import annotations
import copy
import logging
from typing import Callable, Dict, List

# Local Modules
from .Action import Action, ActionType
from .Country import Country
from .TransformTemplate import TransformTemplate

def determine_country_states(country_states: Dict[str, Country], transform_template: TransformTemplate, target_country: Country) -> Dict[str, Country]:
  logging.debug(determine_country_states.__name__)
  new_country_states = copy.deepcopy(country_states)
  country = new_country_states[target_country.name]

  logging.debug("Evaluating {} transform for {}".format(transform_template.name, country.name))

  for input in transform_template.inputs:
    resource_name = input.name
    resource_quantity = input.quantity

    resource = country.resources.get(resource_name)
    resource.quantity -= resource_quantity

    country.resources[resource_name] = resource

  for output in transform_template.outputs:
    resource_name = output.name
    resource_quantity = output.quantity

    resource = country.resources.get(resource_name)
    resource.quantity += resource_quantity

    country.resources[resource_name] = resource

  new_country_states[target_country.name] = country
  
  return new_country_states


# TransformTemplates need to be translated into Actions
# These Actions operate on Country as the state
# PRECONDITIONS are created from transform inputs to determine eligibility
# NEXT_STATE would involve subtracting all inputs then adding all outputs
# ACTION_COST is less clear at this stage 
class TransformAction(Action):
  def __init__(self, preconditions: List[Callable[[Dict[str, Country]], bool]], cost: float, next_state_fn: Callable[[Dict[str, Country]], Dict[str, Country]]) -> None:
    super().__init__(preconditions, cost, next_state_fn)
    self.ACTION_TYPE = ActionType.TRANSFORM

  @property
  def TARGET(self) -> Country:
    return self._TARGET

  @TARGET.setter
  def TARGET(self, target: Country):
    self._TARGET = target

  @property
  def TEMPLATE(self) -> TransformTemplate:
    return self._TEMPLATE

  @TEMPLATE.setter
  def TEMPLATE(self, template: TransformTemplate):
    self._TEMPLATE = template

  def get_impacted_countries(self) -> List[Country]:
    return [self.TARGET]

  def to_string(self, self_country: Country) -> str:
    self_name_fn: Callable[[Country], str] = lambda country: "self" if self_country.name == country.name else country.name 
    transform_name = self.TEMPLATE.name
    target_country_name = self_name_fn(self.TARGET)
    input_resources = ["({})".format(str(resource_quantity)) for resource_quantity in self.TEMPLATE.inputs]
    output_resources = ["({})".format(str(resource_quantity)) for resource_quantity in self.TEMPLATE.outputs]
    return "(TRANSFORM {} {} (INPUTS {}) (OUTPUTS {}))".format(transform_name, target_country_name, " ".join(input_resources), " ".join(output_resources))
#     (TRANSFORM C1
# (INPUTS (Population 25)
# (MetallicElements 5)
# (Timber 25)
# (MetallicAlloys 15))
# (OUTPUTS (Housing 5)
# (HousingWaste 5)
# (Population 25)))

  @staticmethod
  def create_from_transform_template(transform_template: TransformTemplate, target_country: Country) -> TransformAction:
    preconditions = []
    for input in transform_template.inputs:
      resource_name = input.name
      resource_quantity = input.quantity
      fn: Callable[[Dict[str, Country]], bool] = lambda countries: countries[target_country.name].has_resource_quantity(resource_name, resource_quantity)
      preconditions.append(fn)

    cost: float = 0.0

    next_state_fn: Callable[[Dict[str, Country]], Dict[str, Country]] = lambda countries: determine_country_states(countries, transform_template, target_country)

    transform_action = TransformAction(preconditions, cost, next_state_fn)
    transform_action.TARGET = target_country
    transform_action.TEMPLATE = transform_template

    return transform_action
