# Standard Libraries
from configparser import ConfigParser
import logging
import math
from typing import Callable, Dict

# Local Modules
from DataTypes import Country, Schedule

# Numeric Constants
SCHEDULE_FAILED_IMPACT=-0.35
SCHEDULE_LENGTH_IMPACT=0.999
LOGISTIC_FUNCTION_MIDPOINT=0
LOGISTIC_FUNCTION_GROWTH=1
FORCE_SELF_ACCEPT=False

class ScheduleEvaluator:
  def __init__(self, initial_state: Dict[str, Country], state_quality_fn: Callable[[Country], float], self_country_name: str) -> None:
    self.initial_state = initial_state
    self.state_quality_fn = state_quality_fn
    self.self_country_name = self_country_name
    self.initial_quality_lookup = {}
    self.schedule_failed_impact = SCHEDULE_FAILED_IMPACT
    self.schedule_length_impact = SCHEDULE_LENGTH_IMPACT
    self.logistic_function_midpoint = LOGISTIC_FUNCTION_MIDPOINT
    self.logistic_function_growth = LOGISTIC_FUNCTION_GROWTH
    self.force_self_accept = FORCE_SELF_ACCEPT

  def configure(self, config: ConfigParser):
    failed_impact = config.getfloat("ScheduleEvaluation", "FailedImpact", fallback=None)
    if failed_impact is not None:
      logging.info(f"ScheduleEvaluator set schedule failed impact to {failed_impact}")
      self.schedule_failed_impact = failed_impact

    length_impact = config.getfloat("ScheduleEvaluation", "LengthImpact", fallback=None)
    if length_impact is not None:
      logging.info(f"ScheduleEvaluator set schedule length impact to {length_impact}")
      self.schedule_length_impact = length_impact
    
    logistic_function_midpoint = config.getfloat("ScheduleEvaluation", "LogisticFunctionMidpoint", fallback=None)
    if logistic_function_midpoint is not None:
      logging.info(f"ScheduleEvaluator set logistic function midpoint to {logistic_function_midpoint}")
      self.logistic_function_midpoint = logistic_function_midpoint

    logistic_function_growth = config.getfloat("ScheduleEvaluation", "LogisticFunctionGrowth", fallback=None)
    if logistic_function_growth is not None:
      logging.info(f"ScheduleEvaluator set logistic function growth to {logistic_function_growth}")
      self.logistic_function_growth = logistic_function_growth

    force_self_accept = config.getboolean("ScheduleEvaluation", "ForceSelfAccept", fallback=None)
    if force_self_accept is not None:
      logging.info(f"ScheduleEvaluator set force self accept to {force_self_accept}")
      self.force_self_accept = force_self_accept

  def _get_initial_state_quality(self, country_name: str) -> float:
    # Lazy build initial quality lookup and don't repeat for subsequent calculations
    start_quality = self.initial_quality_lookup.get(country_name)
    if not start_quality:
      start_state = self.initial_state[country_name]
      logging.debug(start_state)
      start_quality = self.state_quality_fn(start_state)
      self.initial_quality_lookup[country_name] = start_quality
      logging.info(f"Calculated initial quality - {country_name} = {start_quality}")
    
    return start_quality
  
  def _get_current_state_quality(self, country_name: str, schedule: Schedule) -> float:
    end_state = schedule.get_country_state(country_name)
    return self.state_quality_fn(end_state)

  def undiscounted_reward(self, country: Country, schedule: Schedule):
    logging.debug(self.undiscounted_reward.__name__)

    start_quality = self._get_initial_state_quality(country.name)
    logging.debug(f"Start Quality {start_quality}")

    end_quality = self._get_current_state_quality(country.name, schedule)
    logging.debug(f"End Quality {end_quality}")

    undiscounted_reward = end_quality - start_quality
    logging.debug(f"Undiscounted Reward = {undiscounted_reward}")  
    
    return undiscounted_reward

  def discounted_reward(self, country: Country, schedule: Schedule) -> float:
    logging.debug(self.discounted_reward.__name__)
    
    undiscounted_reward = self.undiscounted_reward(country, schedule)
    discount = self.schedule_length_impact ** schedule.get_steps()
    discounted_reward = float(undiscounted_reward * discount)
    logging.debug(f"Discounted Reward = {discounted_reward}")

    return discounted_reward

  def logistic_function(self, x: float) -> float:
    '''See https://en.wikipedia.org/wiki/Logistic_function'''

    # Supremum (Least Upper Bound) of a probability (0-1) would be 1
    L = 1 

    # Midpoint of the function on the x-axis
    # shifting negative makes success more likely
    # shifting positive makes success less likely
    # zero is neutral, where if x (discounted reward) is also 0, success is 50/50
    x_0 = self.logistic_function_midpoint

    # Function's exponential growth or steepness
    # Negative values invert the curve, interpreting negative DR as success (bad)
    # Increasing the (positive) value increases the impact changes in DR have on probability 
    k = self.logistic_function_growth

    try:
      exponent =  ( -k * ( x - x_0 ) )
      power = math.e ** exponent
    except OverflowError:
      power = float("inf")

    return float( L / ( 1 + power ) )

  def logistic_success(self, country: Country, schedule: Schedule) -> float:
    logging.debug(self.logistic_success.__name__)

    if self.force_self_accept and self.self_country_name == country.name:
      return 1
    
    discounted_reward = self.discounted_reward(country, schedule)
    return self.logistic_function(discounted_reward)

  def country_schedule_success_probability(self, country: Country, schedule: Schedule) -> float:
    return self.logistic_success(country, schedule)

  def schedule_success_probability(self, schedule: Schedule) -> float:
    logging.debug(self.schedule_success_probability.__name__)
    countries = schedule.get_impacted_countries()
    prob = 1
    for country in countries:
      prob = prob * self.country_schedule_success_probability(country, schedule)
    return prob
  
  def log_country_probabilities(self, schedule: Schedule):
    logging.debug(self.log_country_probabilities.__name__)
    countries = schedule.get_impacted_countries()

    for country in countries:
      prob = self.country_schedule_success_probability(country, schedule)
      logging.info(f"Country Schedule Success - {country.name} {(prob*100):.2f}%")

  def log_country_states_diff(self, schedule: Schedule):
    logging.debug(self.log_country_states_diff.__name__)
    countries = schedule.get_impacted_countries()

    for country in countries:
      start_state = self.initial_state.get(country.name)
      final_state = schedule.node.STATE.get(country.name)
      diff = Country.diff_resource_quantities(start_state, final_state)
      undiscounted_reward = self.undiscounted_reward(country, schedule)
      logging.info(f"Country State Diff - {country.name} {diff}")
      logging.info(f"Country State Quality Change - {country.name} {undiscounted_reward}")

  def expected_utility(self, country: Country, schedule: Schedule) -> float:
    logging.debug(self.expected_utility.__name__)
    
    discounted_reward = self.discounted_reward(country, schedule)
    success_probability = self.schedule_success_probability(schedule)
    failure_probability = 1-success_probability

    logging.debug(f"EU Success Probability {success_probability}")
    logging.debug(f"EU Failure Probability {failure_probability}")

    expected_utility = float((success_probability * discounted_reward) + (failure_probability * self.schedule_failed_impact))
    logging.debug(f"Expected Utility = {expected_utility}")

    return expected_utility
