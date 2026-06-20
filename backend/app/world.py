"""
World grid data structure for the AI Civilization Simulator.

Milestone 0: A simple 50x50 grid of cells, each with a biome type.
No simulation logic — just the data structure and serialization.
"""

import random
from enum import Enum
from typing import List, Dict, Any


class BiomeType(str, Enum):
    """Terrain types for world grid cells."""
    GRASS = "grass"
    WATER = "water"
    FOREST = "forest"
    MOUNTAIN = "mountain"


# Color mapping sent to the frontend for canvas rendering
BIOME_COLORS: Dict[BiomeType, str] = {
    BiomeType.GRASS: "#2d4a2d",
    BiomeType.WATER: "#1a3a5c",
    BiomeType.FOREST: "#1b3d1b",
    BiomeType.MOUNTAIN: "#4a4a4a",
}


class Cell:
    """A single cell in the world grid."""

    __slots__ = ("x", "y", "biome")

    def __init__(self, x: int, y: int, biome: BiomeType = BiomeType.GRASS):
        self.x = x
        self.y = y
        self.biome = biome

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "biome": self.biome.value,
        }


class WorldGrid:
    """
    A 2D grid of cells representing the simulation world.

    Milestone 0: Static grid with no procedural generation.
    All cells default to GRASS biome.
    """

    def __init__(self, width: int = 50, height: int = 50):
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []
        self._generate()

    def _generate(self) -> None:
        """Generate a simple random terrain grid."""
        random.seed(42)  # Deterministic seed for reproducibility
        for y in range(self.height):
            row: List[Cell] = []
            for x in range(self.width):
                # Simple random biome assignment for M0 visualization
                roll = random.random()
                if roll < 0.60:
                    biome = BiomeType.GRASS
                elif roll < 0.75:
                    biome = BiomeType.FOREST
                elif roll < 0.88:
                    biome = BiomeType.WATER
                else:
                    biome = BiomeType.MOUNTAIN
                row.append(Cell(x, y, biome))
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        raise IndexError(f"Cell ({x}, {y}) is out of bounds for {self.width}x{self.height} grid")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full world state for initial WebSocket payload."""
        return {
            "width": self.width,
            "height": self.height,
            "biome_colors": {k.value: v for k, v in BIOME_COLORS.items()},
            "cells": [
                [cell.biome.value for cell in row]
                for row in self.cells
            ],
        }
