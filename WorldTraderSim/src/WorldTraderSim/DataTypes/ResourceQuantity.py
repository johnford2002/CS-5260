# Standard Libraries
from dataclasses import dataclass, field

@dataclass
class ResourceQuantity:
  name: str = field()
  quantity: int = field()

  def __str__(self) -> str:
    return "{} {}".format(self.name, self.quantity)
