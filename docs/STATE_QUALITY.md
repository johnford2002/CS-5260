# State Quality  

## Overview

The state quality of a country is determined by each student, though you can share quality functions on the Discussion Forum and in-class in a form that is comprehensible to others, but not in the form of code. Your state quality function, whatever it is, must be substantively dependent on a country’s resources. For example, one state quality function could be a weighted sum of resource factors, and it could be normalized by the population resource, such as wRi ∗ cRi ∗ ARi/AP opulation, where ARi is the amount of a resource, and cRi is a proportionality constant (e.g., 2 units food per person, 0.5 houses per person). Or the quality function could be an [ecological footprint](https://www.footprintnetwork.org/our-work/ecological-footprint/) that is normalized by the AvailableLand resource. State Quality could take other forms as well.
  
In any case, some kind of weighting of resources will likely be important. Your choice of state quality function should be informed by one or more sources of what are [relevant measures](https://tradingeconomics.com/indicators) of country health in the real world (though avoid getting “into the weeds”), and you can share these sources over the Discussion Forum or live in class. Generally, I expect and hope that you will share your ideas on state quality freely on the Programming Project Discussion Forum. 

## Initial Proposal

For part 1, I want my AI agent to attempt to optimize for the following:

* A HOUSING ratio of 2 POPULATION / 1 HOUSING
  * This is overly simplistic when not considering available land, but it should provide a balancing point between 1-person and a family living in a house. Density is something to consider exploring later.
* Limit waste products in order of perceived most harmful to least
  * MetallicAlloysWaste, ElectronicsWaste, HousingWaste
  * Attempting to convey more harmful industrial processes have to be taken into consideration
  * This can potentially feed into recycling in part 2
    * Electronics Waste may be re-used to form new Electronics
    * HousingWaste
* An ELECTRONICS ratio of 1 POPULATION / 1 ELECTRONICS
  * This is far below what might be considered the modern era ratio
  * How many devices do you own? (I can see a dozen+ in front of me right now.)
    * It's going to be interesting to see this working in opposition to the waste concerns
