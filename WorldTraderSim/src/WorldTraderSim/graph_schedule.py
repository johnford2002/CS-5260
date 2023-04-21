# Standard Libraries
import argparse
import json
import logging
import os
from typing import Callable, Dict, List

# External Dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CWD_PATH = os.path.abspath(os.getcwd())
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")


def graph_schedule(args):
  sns.set(font_scale=1.25)
  a4_dims = (11.7, 8.27)
  fig, ax = plt.subplots(figsize=a4_dims)

  ax.grid(False)
  ax.text(x=0.5, y=1.06, s='Expected Utility vs State Quality', fontsize=20, weight='bold', ha='center', va='bottom', transform=ax.transAxes)

  df = pd.read_csv(os.path.join(args.schedules_dir, "best_solution.csv"))
  
  sns.lineplot(x="step", y="expected_utility", data=df, color="b", ax=ax, label="Expected Utility")
  ax.set_xlabel("Depth")
  ax.set_ylabel("Expected Utility")

  ax2 = plt.twinx()
  ax2.grid(False)
  sns.lineplot(x="step", y="state_quality", data=df, color="g", ax=ax2, label="State Quality")
  ax2.set_ylabel("State Quality")
  ax2.legend(loc="upper right")
  
  plt.savefig(os.path.join(args.schedules_dir, "best_solution.png"))


def parseCmdLineArgs():
  parser = argparse.ArgumentParser (description="WorldTraderSim")

  # Arguments governing file paths
  parser.add_argument ("-s", "--schedules-dir", default=DATA_PATH+"/schedules/", help="Directory containing schedule files")
  parser.add_argument ("-o", "--output-file", default="schedules.txt", help="Output file to save graph")

  # Logging level
  parser.add_argument ("-l", "--logging-level", type=int, default=logging.INFO, choices=[logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL], help="logging level, choices 10,20,30,40,50: default 10=logging.DEBUG")
  
  return parser.parse_args()

def main(): 
  logging.info("Graphing WorldTraderSim best schedule...")
  args = parseCmdLineArgs ()
  logging.getLogger().setLevel(args.logging_level)

  graph_schedule(args)

if __name__ == "__main__":
    # set underlying default logging capabilities
  logging.basicConfig (level=logging.DEBUG,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  main()
