# Standard Libraries
from dataclasses import dataclass, field
from typing import List

# Local Modules
from .ResourceQuantity import ResourceQuantity

@dataclass
class TransformTemplate:
  name: str = field(default="")
  inputs: List[ResourceQuantity] = field(default_factory=list)
  outputs: List[ResourceQuantity] = field(default_factory=list)
