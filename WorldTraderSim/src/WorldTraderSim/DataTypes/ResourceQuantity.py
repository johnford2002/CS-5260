# Standard Libraries
from dataclasses import dataclass, field
import json

@dataclass
class ResourceQuantity:
  name: str = field()
  quantity: int = field()

  def __iter__(self):
    yield from {
      "name": self.name,
      "quantity": self.quantity
    }.items()

  def __str__(self) -> str:
    return "{} {}".format(self.name, self.quantity)
