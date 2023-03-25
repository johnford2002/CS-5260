#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Union

from .Action import ActionType
from .Node import Node
from .Country import Country
from .TransferAction import TransferAction
from .TransformAction import TransformAction

class Solution(object):

  NODE: Node
  PATH: List[Node]
  VISITED: List[Country]

  def __init__(self, goal_node: Node, visited_nodes: List[Country]) -> None:
    super().__init__()
    self.NODE = goal_node
    self.PATH = []
    current_node = goal_node
    while current_node is not None:
      self.PATH.append(current_node)
      current_node = current_node.PARENT
    self.PATH.reverse()
    self.VISITED = visited_nodes

  def print_path(self):
    step = 1
    for node in self.PATH:
      print("Step {}".format(step))
      last_action: Union[TransferAction, TransformAction] = node.PARENT_ACTION
      last_action_type = last_action and last_action.ACTION_TYPE
      action_details = ""
      if last_action_type == ActionType.TRANSFER:
        sender = last_action.SENDER.name
        receiver = last_action.RECEIVER.name
        resource_quantities = last_action.RESOURCE_QUANTITIES
        quantities = ""
        for resource_quantity in resource_quantities:
          if quantities != "":
            quantities += "; "
          quantities += "{} - {}".format(resource_quantity.name, resource_quantity.quantity)
          action_details = "Sender: {}, Receiver: {}, Quantities: {}".format(sender, receiver, quantities)
      elif last_action_type == ActionType.TRANSFORM:
        template = last_action.TEMPLATE
        action_details = template.name
      if last_action_type:
        print("{} = {}".format(last_action_type, action_details))
      else:
        print("No Last Action")
      step += 1

  def print_visited_order(self):
    print('Visited Nodes: ', end='')
    for node in self.VISITED[:-1]:
      print('{} -> '.format(node), end='')
    print('{}'.format(self.VISITED[-1]))
