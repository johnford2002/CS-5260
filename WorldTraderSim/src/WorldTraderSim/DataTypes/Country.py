# Standard Libraries
from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import Dict, List

# Local Modules
from .ResourceQuantity import ResourceQuantity

@dataclass
class Country:
  name: str = field()
  resources: Dict[str, ResourceQuantity] = field(default_factory=dict)

  def __iter__(self):
    yield from {
      "name": self.name,
      "resources": json.dumps([dict(resource) for resource in self.resources.values()])
    }.items()

  def __str__(self) -> str:
    return json.dumps(dict(self))

  @staticmethod
  def from_dict(data: Dict):
    country_name = data.get("Country")
    del data["Country"]

    resource_quantities = {}
    for key in data.keys():
      resource_quantities[key] = ResourceQuantity(name=key, quantity=int(data[key]))

    return Country(
      name=country_name,
      resources=resource_quantities
    )
  
  @staticmethod
  def diff_resource_quantities(start_state: Country, final_state: Country) -> List[ResourceQuantity]:
    start_resources = start_state.resources
    final_resurces = final_state.resources

    changes = []
    for resource_name, final_quantity in final_resurces.items():
      start_quantity = start_resources[resource_name]
      change = final_quantity.quantity - start_quantity.quantity
      if change:
        changes.append(ResourceQuantity(resource_name, change))
    return changes

  @staticmethod
  def print_resource_quantities(resource_quantities: List[ResourceQuantity]):
    for resource_quantity in resource_quantities:
      print("{} changed by {}".format(resource_quantity.name, resource_quantity.quantity))

  def has_resource_quantity(self, resource_name: str, resource_quantity: int) -> bool:
    return (self.resources.get(resource_name).quantity >= resource_quantity)
