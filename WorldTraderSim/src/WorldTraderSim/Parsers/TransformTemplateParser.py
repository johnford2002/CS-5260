# Standard Libraries
from dataclasses import dataclass, field
import os
import re
from typing import List

# Local Modules
import Constants
from DataTypes import ResourceQuantity
from DataTypes import TransformTemplate

@dataclass
class ResourceQuantity:
  name: str = field()
  quantity: int = field()

@dataclass
class TransformTemplate:
  name: str = field(default="")
  inputs: List[ResourceQuantity] = field(default_factory=list)
  outputs: List[ResourceQuantity] = field(default_factory=list)

def read_file(file_path: str) -> List[dict]:
  file_contents = None
  with open(file_path, mode='r') as file:
    file_contents = file.read()
  return file_contents

def validate_nonempty(template: str = "") -> bool:
  return template != ""

def validate_enclosed(template: str = "") -> bool:
  left_paren_count = template.count("(")
  right_paren_count = template.count(")")
  if left_paren_count != right_paren_count:
    return False
  return True

def validate_keywords(template: str = "") -> bool:
  for keyword in Constants.TRANSFORM_KEYWORDS:
    if not keyword in template:
      return False
  return True

def validate(template: str = ""):
  if not validate_nonempty(template):
    raise Exception("Empty template")
  if not validate_enclosed(template):
    raise Exception("Incorrect parentheses counts, verify all expressions are properly enclosed")
  elif not validate_keywords(template):
    raise Exception("Missing required keywords, verify transform is syntactically correct")

def build_resource_quantities(resource_quantities_block):
  quantities = []

  regex = r"\(([A-Za-z]+) (\d)\)"
  matches = re.finditer(regex, resource_quantities_block, re.MULTILINE)
  for match in matches:
      resource_name, resource_quantity = match.groups()
      quantities.append(ResourceQuantity(name=resource_name, quantity=int(resource_quantity)))

  return quantities

def build_transform_template(template_path: str, template: str) -> TransformTemplate:
  transform = TransformTemplate()
  
  basename = os.path.basename(template_path)
  transform_name = os.path.splitext(basename)[0]
  transform.name = transform_name

  inputs_start = template.index("INPUTS")
  outputs_start = template.index("OUTPUTS")

  inputs_string = template[inputs_start:outputs_start]
  outputs_string = template[outputs_start:]

  transform.inputs = build_resource_quantities(inputs_string)
  transform.outputs = build_resource_quantities(outputs_string)

  return transform

def parse(template_path: str) -> dict:
  template = read_file(template_path)
  validate(template)
  transform_template = build_transform_template(template_path, template)
  return transform_template
