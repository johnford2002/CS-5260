Sample AI Search Strategy Code for CS 5260
==========================================

Overview
--------

This repository holds sample code to illustrate one potential methodology for organizing your code in a way such that it is relatively simple to try out different search strategies, implement your own state spaces, and define your own set of actions and/or heuristics.

Note that most of this code is centered around carrying out searches using the methodologies discussed in Weeks 1 and 2 of the CS 5260 course, and as such, it does not implement more advanced concepts, such as factored representations for state, utility-based searches, adversarial searches, etc. This is **only** intended to give students an idea of how it is possible to formulate your problems in a way that allows you to explore different strategies with relative ease.


Installation
------------

The easiest way to install this library is in *developer mode* which allows you to make changes to the code that will automatically be picked up by your Python environment. You can do this by cloning the repository to your hard drive and issuing the following command from the ``CS5260`` directory in a terminal:

``python3 -m pip install -e .``


Usage
-----

Once installed, you are free to explore the various search-based primitives and data types under the ``DataTypes`` subdirectory. The ``SearchStrategies`` directory contains a number of pre-implemented, basic search strategies for illustrative purposes. Finally, the ``Examples`` directory contains a script called ``HW2_1.py`` that you can use to test carrying out a number of search strategies that we've covered so far on the explicit graph defined in the Week 2 homework.

To run this script, simply issue the following command:

``python3 -m cs5260.Examples.HW2_1``
