# Standard Libraries
from dataclasses import dataclass, field

@dataclass
class ResourceQuantity:
  name: str = field()
  quantity: int = field()
