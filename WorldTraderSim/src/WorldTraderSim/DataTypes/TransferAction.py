#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Libraries
from __future__ import annotations
import copy
from enum import Enum
import logging
from typing import Callable, Dict, List

# Local Modules
from .Action import Action, ActionType
from .Country import Country
from .ResourceQuantity import ResourceQuantity

class TransferDirection(Enum):
  SEND = 1
  RECEIVE = 2

  @staticmethod
  def determine_sending_country(transfer_direction: TransferDirection, self_country: Country, other_country: Country) -> Country:
    if transfer_direction == TransferDirection.SEND:
      return self_country
    elif transfer_direction == TransferDirection.RECEIVE:
      return other_country
    else:
      raise Exception("Unrecognized Transfer Direction")

  @staticmethod
  def determine_receiving_country(transfer_direction: TransferDirection, self_country: Country, other_country: Country) -> Country:
    if transfer_direction == TransferDirection.SEND:
      return other_country
    elif transfer_direction == TransferDirection.RECEIVE:
      return self_country
    else:
      raise Exception("Unrecognized Transfer Direction")

# Runtime
def determine_country_states(self_country: Country, other_country: Country, country_states: Dict[str, Country], resource_quantities: List[ResourceQuantity], transfer_direction: TransferDirection) -> Dict[str, Country]:
  logging.debug(determine_country_states.__name__)
  new_country_states = copy.deepcopy(country_states)

  sender_country = TransferDirection.determine_sending_country(transfer_direction, self_country, other_country)
  receiver_country = TransferDirection.determine_receiving_country(transfer_direction, self_country, other_country) 
  sender = new_country_states[sender_country.name]
  receiver = new_country_states[receiver_country.name]

  for resource_quantity in resource_quantities:
    name = resource_quantity.name
    quantity = resource_quantity.quantity

    logging.debug("Evaluating a transfer of {} {} from {} to {}".format(quantity, name, sender.name, receiver.name))

    sender_resource = sender.resources.get(name)
    sender_resource.quantity -= quantity
    sender.resources[name] = sender_resource
    new_country_states[sender.name] = sender

    receiver_resource = receiver.resources.get(name)
    receiver_resource.quantity += quantity
    receiver.resources[name] = receiver_resource
    new_country_states[receiver.name] = receiver

  return new_country_states

# Transfers
# Are from one country to another country, constituting one transfer (turn or step)
# Experiment with varied amounts of resources
# (1 Timber, 5 Timber, 100 Timber, etc.) 
# Experiment with varied resource types 
# (only send wood, send wood and metal, send wood and metal and water, etc.)
# Caution - More variety = Higher branching factor (potentially longer processing)


# Transfers need to be translated into Actions
# These Actions operate on Country as the state
# PRECONDITIONS are created from resource quantities
#     1 to N #TODO
#     Single or Multi
# NEXT_STATE would involve subtracting or adding quantities depending on direction
# ACTION_COST is less clear at this stage 
class TransferAction(Action):
  def __init__(self, preconditions: List[Callable[[List[Country]], bool]], cost: float, next_state_fn: Callable[[Dict[str, Country]], Dict[str, Country]]) -> None:
    super().__init__(preconditions, cost, next_state_fn)
    self.ACTION_TYPE = ActionType.TRANSFER

  @property
  def SENDER(self) -> Country:
    return self._SENDER

  @SENDER.setter
  def SENDER(self, sender: Country):
    self._SENDER = sender

  @property
  def RECEIVER(self) -> Country:
    return self._RECEIVER

  @RECEIVER.setter
  def RECEIVER(self, receiver: Country):
    self._RECEIVER = receiver

  @property
  def DIRECTION(self) -> TransferDirection:
    return self._DIRECTION

  @DIRECTION.setter
  def DIRECTION(self, direction: TransferDirection):
    self._DIRECTION = direction

  @property
  def RESOURCE_QUANTITIES(self) -> List[ResourceQuantity]:
    return self._RESOURCE_QUANTITIES

  @RESOURCE_QUANTITIES.setter
  def RESOURCE_QUANTITIES(self, resource_quantities: List[ResourceQuantity]):
    self._RESOURCE_QUANTITIES = resource_quantities

  def get_impacted_countries(self) -> List[Country]:
    return [self.SENDER, self.RECEIVER]

  def to_string(self, self_country: Country) -> str:
    # (TRANSFER self C2 ((Housing 3))) EU: S_2
    self_name_fn: Callable[[Country], str] = lambda country: "self" if self_country.name == country.name else country.name 
    sending_country_name = self_name_fn(self.SENDER)
    receiving_country_name = self_name_fn(self.RECEIVER) 
    resources = ["({})".format(str(resource_quantity)) for resource_quantity in self.RESOURCE_QUANTITIES]
    return "(TRANSFER {} {} ({}))".format(sending_country_name, receiving_country_name, " ".join(resources))

  # Build Time
  @staticmethod
  def create_from_resource_quantities(resource_quantities: List[ResourceQuantity], transfer_direction: TransferDirection, self_country: Country, other_country: Country, cost_fn: Callable[[List[Country]], float]) -> TransferAction:
    sending_country = TransferDirection.determine_sending_country(transfer_direction, self_country, other_country)
    receiving_country = TransferDirection.determine_receiving_country(transfer_direction, self_country, other_country) 

    preconditions = []
    for resource_quantity in resource_quantities:
      name = resource_quantity.name
      quantity = resource_quantity.quantity
      fn: Callable[[Dict[str, Country]], bool] = lambda countries: countries[sending_country.name].has_resource_quantity(name, quantity)
      preconditions.append(fn)

    next_state_fn: Callable[[Dict[str, Country]], Dict[str, Country]] = lambda countries: determine_country_states(self_country, other_country, countries, resource_quantities, transfer_direction)

    # This seems like it should be something like the delta between current state and next state
    # As viewed by the state quality function (Heuristic)
    # However, that might be considered path cost instead, not clear
    cost: float = 0.0

    transfer_action = TransferAction(preconditions, cost, next_state_fn)
    transfer_action.SENDER = sending_country
    transfer_action.RECEIVER = receiving_country
    transfer_action.DIRECTION = transfer_direction
    transfer_action.RESOURCE_QUANTITIES = resource_quantities

    return transfer_action
