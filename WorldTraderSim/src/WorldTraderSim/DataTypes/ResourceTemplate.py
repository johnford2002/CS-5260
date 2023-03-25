# Standard Libraries
from dataclasses import dataclass, field

NONTRANSFERABLE_RESOURCES = [
  "Population"
]

@dataclass
class ResourceTemplate:
  name: str = field()
  weight: float = field()
  factor: str = field()

  @staticmethod
  def from_dict(data):
    return ResourceTemplate(
      name=data.get("Resource"),
      weight=float(data.get("Weight")),
      factor=data.get("Factor")
    )

  def transferable(self) -> bool:
    return self.name not in NONTRANSFERABLE_RESOURCES
