# Standard Libaries
from typing import List

# Local Modules
from DataTypes import Country
from DataTypes import ResourceTemplate

class StateEvaluator:
  def __init__(self, resources: List[ResourceTemplate]) -> None:
    self.resources = resources
    self.resource_weights = {}
    self.resource_factors = {}
    self._build_resouce_maps()

  def _build_resouce_maps(self):
    for resource in self.resources:
      self.resource_weights[resource.name] = resource.weight
      self.resource_factors[resource.name] = resource.factor

  def weighted_sum(self, country_state: Country) -> float:
    country_resources = country_state.resources.values()

    weighted_sum = 0.0
    for resource_quantity in country_resources:
      resource_amount = resource_quantity.quantity
      resource_weight = self.resource_weights[resource_quantity.name]
      weighted_sum = weighted_sum + (resource_amount * resource_weight)

    return weighted_sum

  def state_quality(self, country_state: Country) -> float:
    return self.weighted_sum(country_state)
