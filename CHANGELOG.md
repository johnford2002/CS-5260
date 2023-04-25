# Changelog

## Part1 -> Part2

### Fixes
* ScheduleEvaluator
  * Fix incorrect constant usage of gamma (schedule length impact)
* TemplateParser
  * Allow using numbers in resource names

### Improvements
* Node
  * Cache `STATE_HASH` to reduce redundant hashing
  * Cache `DEPTH` to avoid recounting links
* ScheduleEvaluator
  * Cache initial state quality to avoid repeated recalculation
  * Simplify equations for better readability
  * Allow configuration of calculation variables
* TransformAction
  * Allow specifying `quantity_max` to be used as a multiplier
  * Create list of transform actions up to max
  * Update printing to reflect multiplier changes
* Configuration
  * Expose `TransferQuantityMax` & `TransformQuantityMax`
  * Expose new section `ScheduleEvaluation`

### Additions
* Calculations based on Balanced Resources starting point
* Ignore Population since it's equivalent in/out
* Housing2 & Housing3
  * Housing Net
    * Housing Input = Timber (5x0.015) + MetallicElements (0.025) + MetallicAlloys (3x0.2) = 0.7
    * Housing Output = Housing (0.9) + HousingWaste (-0.15) = 0.75
    * Net = 0.75 - 0.7 = 0.05
  * Housing2 Net
    * Housing2 Input = Housing (0.9) + Timber (0.015) + MetallicElements (0.025) + MetallicAlloys (0.2) = 1.14
    * Housing2 Output = Housing2 (1.4) + HousingWaste (-0.15) = 1.25
    * Net = 1.25 - 1.14 = 0.11
  * Housing3 Net
    * Housing3 Input = Housing2 (1.4) + Timber (0.015) + MetallicElements (0.025) + MetallicAlloys (0.2) = 1.64
    * Housing3 Output = Housing3 (1.82) + HousingWaste (-0.15) = 1.67
    * Net = 1.67 - 1.64 = 0.03
* Electronics2 & Electronics3
  * Electronics Net
    * Electronics Input = MetallicElements (3x0.025) + MetallicAlloys (2x0.2) = 0.475
    * Electronics Output = Electronics (2x0.35) + ElectronicsWaste (-0.2) = 0.5
    * Net = 0.5 - 0.475 = 0.025
  * Electronics2 Net
    * Electronics2 Input = Electronics (0.35) + MetallicElements (0.025) + MetallicAlloys (0.2) = 0.575
    * Electronics2 Output = Electronics2 (0.825) + ElectronicsWaste (-0.2) = 0.625
    * Net = 0.625 - 0.575 = 0.05
  * Electronics3 Net
    * Electronics3 Input = Electronics2 (0.825) + MetallicElements (0.025) + MetallicAlloys (0.2) = 1.05
    * Electronics3 Output = Electronics3 (1.27) + ElectronicsWaste (-0.2) = 1.07
    * Net = 1.07 - 1.05 = 0.02
