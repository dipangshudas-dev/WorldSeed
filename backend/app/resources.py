"""
Resource node system for the AI Civilization Simulator.

Milestone 1:
  - ResourceType enum (FOOD, WOOD, STONE)
  - ResourceNode data class (static, no harvesting/depletion)
  - generate_resources() — places nodes on biome-appropriate tiles

Resources are independent entities that live on the WorldGrid,
not embedded inside Cell objects (per system design layer separation).
"""

import random
from enum import Enum
from typing import List, Dict, Any


class ResourceType(str, Enum):
    """Material types for resource nodes."""
    FOOD = "food"
    WOOD = "wood"
    STONE = "stone"


# ---------------------------------------------------------------------------
# Resource templates — maps (type, name, biomes_allowed)
# ---------------------------------------------------------------------------

_FOOD_TEMPLATES = [
    ("Berry Bush", {"grass"}),
    ("Wild Food Patch", {"grass", "forest"}),
]

_WOOD_TEMPLATES = [
    ("Tree Cluster", {"forest"}),
    ("Lumber Resource", {"forest", "grass"}),  # forest edges
]

_STONE_TEMPLATES = [
    ("Stone Deposit", {"mountain"}),
    ("Rock Cluster", {"mountain", "grass"}),  # mountain edges
]


class ResourceNode:
    """
    A static resource node placed on the world grid.

    Milestone 1: Visualisation only — no harvesting, depletion,
    or regeneration mechanics.
    """

    __slots__ = ("id", "x", "y", "resource_type", "name")

    def __init__(
        self,
        node_id: int,
        x: int,
        y: int,
        resource_type: ResourceType,
        name: str,
    ):
        self.id = node_id
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "type": self.resource_type.value,
            "name": self.name,
        }


# ---------------------------------------------------------------------------
# Placement logic
# ---------------------------------------------------------------------------


def _get_neighbors(x: int, y: int, width: int, height: int) -> List[tuple]:
    """Return valid orthogonal + diagonal neighbor coordinates."""
    neighbors = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
    return neighbors


def generate_resources(
    cells: list,
    width: int,
    height: int,
    rng: random.Random,
) -> List[ResourceNode]:
    """
    Place resource nodes on biome-appropriate tiles.

    Placement rules:
      - Food:  ~12% of grassland tiles near forest borders + scattered
      - Wood:  ~18% of forest tiles
      - Stone: ~20% of mountain tiles + some adjacent grass tiles

    Parameters
    ----------
    cells  : 2D list of Cell objects (cells[y][x])
    width  : Grid width
    height : Grid height
    rng    : Seeded Random instance for reproducibility

    Returns
    -------
    List of ResourceNode instances.
    """
    nodes: List[ResourceNode] = []
    next_id = 1

    # Build a quick biome lookup grid (string values)
    biome_grid = [[cells[y][x].biome.value for x in range(width)] for y in range(height)]

    # Helper: check if a tile has a specific biome neighbor
    def has_neighbor_biome(x: int, y: int, biome: str) -> bool:
        for nx, ny in _get_neighbors(x, y, width, height):
            if biome_grid[ny][nx] == biome:
                return True
        return False

    for y in range(height):
        for x in range(width):
            biome = biome_grid[y][x]

            # --- FOOD ---
            if biome == "grass":
                # Higher chance near forest edges
                chance = 0.14 if has_neighbor_biome(x, y, "forest") else 0.06
                if rng.random() < chance:
                    template = rng.choice(_FOOD_TEMPLATES)
                    if biome in template[1]:
                        nodes.append(ResourceNode(next_id, x, y, ResourceType.FOOD, template[0]))
                        next_id += 1

            # --- WOOD ---
            if biome == "forest":
                if rng.random() < 0.18:
                    template = rng.choice(_WOOD_TEMPLATES)
                    nodes.append(ResourceNode(next_id, x, y, ResourceType.WOOD, template[0]))
                    next_id += 1
            elif biome == "grass" and has_neighbor_biome(x, y, "forest"):
                # Lumber at forest edges
                if rng.random() < 0.05:
                    nodes.append(ResourceNode(next_id, x, y, ResourceType.WOOD, "Lumber Resource"))
                    next_id += 1

            # --- STONE ---
            if biome == "mountain":
                if rng.random() < 0.20:
                    template = rng.choice(_STONE_TEMPLATES)
                    nodes.append(ResourceNode(next_id, x, y, ResourceType.STONE, template[0]))
                    next_id += 1
            elif biome == "grass" and has_neighbor_biome(x, y, "mountain"):
                if rng.random() < 0.06:
                    nodes.append(ResourceNode(next_id, x, y, ResourceType.STONE, "Rock Cluster"))
                    next_id += 1

    return nodes
