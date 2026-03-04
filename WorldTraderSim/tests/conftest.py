"""
Shared pytest fixtures and sys.path configuration for WorldTraderSim tests.

The source code uses bare imports like `from DataTypes import Country`, so the
application source directory must be on sys.path before any test imports occur.
"""
import os
import sys

import pytest

# Make all application modules importable without package prefix
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "WorldTraderSim"))

from DataTypes import Country, ResourceQuantity, ResourceTemplate, TransformTemplate


@pytest.fixture
def basic_resources():
    """Nine standard resources matching resources-balanced.csv weights."""
    return [
        ResourceTemplate(name="Population", weight=0.3, factor=""),
        ResourceTemplate(name="MetallicElements", weight=0.025, factor=""),
        ResourceTemplate(name="Timber", weight=0.015, factor=""),
        ResourceTemplate(name="MetallicAlloys", weight=0.2, factor=""),
        ResourceTemplate(name="MetallicAlloysWaste", weight=-0.1, factor=""),
        ResourceTemplate(name="Electronics", weight=0.35, factor=""),
        ResourceTemplate(name="ElectronicsWaste", weight=-0.2, factor=""),
        ResourceTemplate(name="Housing", weight=0.9, factor=""),
        ResourceTemplate(name="HousingWaste", weight=-0.15, factor=""),
    ]


@pytest.fixture
def atlantis():
    """Balanced starting country with metals and timber but no manufactured goods."""
    return Country(
        name="Atlantis",
        resources={
            "Population": ResourceQuantity("Population", 100),
            "MetallicElements": ResourceQuantity("MetallicElements", 100),
            "Timber": ResourceQuantity("Timber", 50),
            "MetallicAlloys": ResourceQuantity("MetallicAlloys", 0),
            "MetallicAlloysWaste": ResourceQuantity("MetallicAlloysWaste", 0),
            "Electronics": ResourceQuantity("Electronics", 0),
            "ElectronicsWaste": ResourceQuantity("ElectronicsWaste", 0),
            "Housing": ResourceQuantity("Housing", 0),
            "HousingWaste": ResourceQuantity("HousingWaste", 0),
        },
    )


@pytest.fixture
def europa():
    """Second country used in multi-country transfer tests."""
    return Country(
        name="Europa",
        resources={
            "Population": ResourceQuantity("Population", 100),
            "MetallicElements": ResourceQuantity("MetallicElements", 50),
            "Timber": ResourceQuantity("Timber", 50),
            "MetallicAlloys": ResourceQuantity("MetallicAlloys", 0),
            "MetallicAlloysWaste": ResourceQuantity("MetallicAlloysWaste", 0),
            "Electronics": ResourceQuantity("Electronics", 0),
            "ElectronicsWaste": ResourceQuantity("ElectronicsWaste", 0),
            "Housing": ResourceQuantity("Housing", 0),
            "HousingWaste": ResourceQuantity("HousingWaste", 0),
        },
    )


@pytest.fixture
def country_states(atlantis, europa):
    return {atlantis.name: atlantis, europa.name: europa}


@pytest.fixture
def alloys_template():
    """Mirrors data/templates/base/alloys.tmpl: 1 Pop + 2 Metal -> 1 Alloy + 1 Waste."""
    return TransformTemplate(
        name="alloys",
        inputs=[
            ResourceQuantity("Population", 1),
            ResourceQuantity("MetallicElements", 2),
        ],
        outputs=[
            ResourceQuantity("Population", 1),
            ResourceQuantity("MetallicAlloys", 1),
            ResourceQuantity("MetallicAlloysWaste", 1),
        ],
    )
