# Standard Libraries
from __future__ import annotations
import csv
from dataclasses import dataclass, field
from os import path, PathLike
from typing import Callable, Dict, List, Union

# Local Modules
from .Country import Country
from .Node import Node
from .Solution import Solution

@dataclass
class Schedule:
  node: Node = field(default_factory=Node)
  countries: List[Country] = field(default_factory=list)

  # Returns the current state of country on the given node
  def get_country_state(self, country_name: str) -> Country:
    return self.node.STATE.get(country_name)

  def get_impacted_countries(self) -> List[Country]:
    if self.countries and len(self.countries):
      return self.countries
    
    found_country_names = {}
    current_node = self.node
    while current_node:
      last_action = current_node.PARENT_ACTION
      if last_action:
        countries = last_action.get_impacted_countries()
        for country in countries:
          if not found_country_names.get(country.name, False):
            found_country_names[country.name] = True
            self.countries.append(country)
      current_node = current_node.PARENT

    return self.countries

  def get_steps(self):
    return self.node.depth()

  @staticmethod
  def write_solutions(solutions: Dict[str, Solution], expected_utility_fn: Callable[[Country, Schedule], float], self_country: Country, output_file_name: str, output_dir: Union[str, PathLike, None] = None):
    if not output_dir:
      module_path = path.dirname(path.abspath(__file__))
      output_dir =  path.join(module_path, "../data/schedules/")

    utilities = sorted(list(solutions.keys()), reverse=True)

    with open(output_dir+output_file_name, "w") as file:
      solutions_count = 0
      for utility in utilities:
        solution = solutions[utility]
        if solutions_count:
          file.write(",\n")
        file.write("[\n")
        for node in solution.PATH:
          if node.PARENT_ACTION:
            eu = expected_utility_fn(self_country, Schedule(node))
            file.write("  " + node.PARENT_ACTION.to_string(self_country) + " EU: {}\n".format(eu))
        file.write("]")
        solutions_count += 1
    
  @staticmethod
  def write_csv(solution: Solution, state_quality_fn: Callable[[Country], float], expected_utility_fn: Callable[[Country, Schedule], float], self_country: Country, output_file_name: str, output_dir: Union[str, PathLike, None] = None):
    if not output_dir:
      module_path = path.dirname(path.abspath(__file__))
      output_dir =  path.join(module_path, "../data/schedules/")

    solution_path = []
    for index, node in enumerate(solution.PATH):
      if node.PARENT_ACTION:
        state_quality = state_quality_fn(node.STATE[self_country.name])
        eu = expected_utility_fn(self_country, Schedule(node))
        solution_path.append({
          "action_type": node.PARENT_ACTION.ACTION_TYPE,
          "step": index+1,
          "expected_utility": eu,
          "state_quality": state_quality,
        })

    with open(path.join(output_dir, output_file_name), 'w', newline='') as file:
      csv_file = csv.DictWriter(file, fieldnames=["action_type", "step", "expected_utility", "state_quality"])

      csv_file.writeheader()
      csv_file.writerows(solution_path)
