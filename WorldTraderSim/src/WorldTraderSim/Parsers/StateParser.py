# Standard Libraries
import csv
import logging
from typing import List

# Local Modules
import Constants

def read_csv(file_path: str) -> List[dict]:
  entries = []
  with open(file_path, mode='r') as file:
    csvFile = csv.DictReader(file)

    for entry in csvFile:
      entries.append(entry)
  
  return entries

def validate_resources(resources: List) -> bool:
  for required in Constants.REQUIRED_RESOURCES:
    if not required in resources:
      logging.error("Missing resource {}".format(required))
      return False
  return True

def validate_initial_state(initial_state: List) -> bool:
  for country in initial_state:
    resources = [resource for resource in country.keys()]
    resources.remove("Country")
    if not validate_resources(resources):
      logging.error("Country {} is missing required resources".format(country.get("Country")))
      return False
  return True
