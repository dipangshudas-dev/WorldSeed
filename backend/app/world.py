"""
World grid data structure for the AI Civilization Simulator.

Milestone 1: Procedural terrain generation using multi-octave value noise.
  - Elevation map  → mountains vs water
  - Moisture map   → forest vs grassland
  - River carving  → visual rivers flowing downhill
  - Forest smoothing → cellular automata pass for natural clusters
  - Resource nodes → static entities placed on biome-appropriate tiles

The world generates once at startup. No per-tick recalculation.
"""

import random
import math
from enum import Enum
from typing import List, Dict, Any, Optional

from app.noise import fractal_noise
from app.resources import generate_resources, ResourceNode


class BiomeType(str, Enum):
    """Terrain types for world grid cells."""
    GRASS = "grass"
    WATER = "water"
    FOREST = "forest"
    MOUNTAIN = "mountain"


# Color mapping sent to the frontend for canvas rendering
BIOME_COLORS: Dict[BiomeType, str] = {
    BiomeType.GRASS: "#2d5a3f",
    BiomeType.WATER: "#1a3a5c",
    BiomeType.FOREST: "#1b4332",
    BiomeType.MOUNTAIN: "#52525b",
}


class Cell:
    """A single cell in the world grid."""

    __slots__ = ("x", "y", "biome", "elevation")

    def __init__(
        self,
        x: int,
        y: int,
        biome: BiomeType = BiomeType.GRASS,
        elevation: float = 0.5,
    ):
        self.x = x
        self.y = y
        self.biome = biome
        self.elevation = elevation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "biome": self.biome.value,
        }


class WorldGrid:
    """
    A 2D grid of cells representing the simulation world.

    Milestone 1: Procedural generation with noise-based terrain,
    river carving, forest smoothing, and resource node placement.
    """

    def __init__(self, width: int = 50, height: int = 50, seed: int = 42):
        self.width = width
        self.height = height
        self.seed = seed
        self.cells: List[List[Cell]] = []
        self.resources: List[ResourceNode] = []
        self._generate()

    # ------------------------------------------------------------------
    # Terrain generation pipeline
    # ------------------------------------------------------------------

    def _generate(self) -> None:
        """
        Full procedural terrain generation pipeline:
          1. Generate elevation & moisture noise maps
          2. Classify biomes from noise values
          3. Smooth forests (cellular automata)
          4. Carve rivers from mountains to water/edge
          5. Place resource nodes
        """
        rng = random.Random(self.seed)

        # Seeds for independent noise layers
        elev_seed = self.seed
        moist_seed = self.seed + 1000

        # ----------------------------------------------------------
        # Step 1: Generate raw noise maps
        # ----------------------------------------------------------
        # Scale controls feature size — lower = larger features.
        # For a 50×50 grid we want large sweeping regions.
        elev_scale = 0.06
        moist_scale = 0.055

        elevation = [[0.0] * self.width for _ in range(self.height)]
        moisture = [[0.0] * self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                elevation[y][x] = fractal_noise(
                    x, y, octaves=6, persistence=0.5,
                    scale=elev_scale, seed=elev_seed,
                )
                moisture[y][x] = fractal_noise(
                    x, y, octaves=4, persistence=0.45,
                    scale=moist_scale, seed=moist_seed,
                )

        # ----------------------------------------------------------
        # Step 2: Apply island mask — fade elevation toward edges
        # to create a landmass surrounded by water
        # ----------------------------------------------------------
        cx, cy = self.width / 2.0, self.height / 2.0
        max_dist = math.sqrt(cx * cx + cy * cy)

        for y in range(self.height):
            for x in range(self.width):
                dx = (x - cx) / cx  # normalised to [-1, 1]
                dy = (y - cy) / cy
                dist = math.sqrt(dx * dx + dy * dy)
                # Gentle falloff — only the outermost ring becomes water
                falloff = max(0.0, 1.0 - dist * 0.55)
                elevation[y][x] = elevation[y][x] * (0.3 + 0.7 * falloff)

        # Re-normalize elevation to [0, 1] after island mask
        # so mountain thresholds can actually be reached
        e_min = min(elevation[y][x] for y in range(self.height) for x in range(self.width))
        e_max = max(elevation[y][x] for y in range(self.height) for x in range(self.width))
        e_range = e_max - e_min if e_max > e_min else 1.0
        for y in range(self.height):
            for x in range(self.width):
                elevation[y][x] = (elevation[y][x] - e_min) / e_range

        # ----------------------------------------------------------
        # Step 3: Classify biomes from elevation + moisture
        # ----------------------------------------------------------
        self.cells = []
        for y in range(self.height):
            row: List[Cell] = []
            for x in range(self.width):
                e = elevation[y][x]
                m = moisture[y][x]

                if e < 0.28:
                    biome = BiomeType.WATER
                elif e > 0.75:
                    biome = BiomeType.MOUNTAIN
                elif m > 0.50:
                    biome = BiomeType.FOREST
                else:
                    biome = BiomeType.GRASS

                row.append(Cell(x, y, biome, elevation=e))
            self.cells.append(row)

        # ----------------------------------------------------------
        # Step 4: Smooth forests — one cellular automata pass
        # Removes isolated forest tiles and fills gaps in clusters
        # ----------------------------------------------------------
        self._smooth_forests()

        # ----------------------------------------------------------
        # Step 5: Carve rivers
        # ----------------------------------------------------------
        self._carve_rivers(elevation, rng)

        # ----------------------------------------------------------
        # Step 6: Place resource nodes
        # ----------------------------------------------------------
        self.resources = generate_resources(
            self.cells, self.width, self.height, rng
        )

    def _smooth_forests(self) -> None:
        """
        Cellular automata pass to create natural forest clusters.

        Rule: A non-water/non-mountain tile becomes forest if ≥4
        of its 8 neighbors are forest. Otherwise it becomes grass.
        Preserves water and mountain tiles.
        """
        # Build snapshot of current biomes
        snapshot = [
            [self.cells[y][x].biome for x in range(self.width)]
            for y in range(self.height)
        ]

        for y in range(self.height):
            for x in range(self.width):
                current = snapshot[y][x]
                # Only modify grass/forest tiles
                if current in (BiomeType.WATER, BiomeType.MOUNTAIN):
                    continue

                forest_count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if snapshot[ny][nx] == BiomeType.FOREST:
                                forest_count += 1

                if forest_count >= 4:
                    self.cells[y][x].biome = BiomeType.FOREST
                elif forest_count <= 1:
                    self.cells[y][x].biome = BiomeType.GRASS

    def _carve_rivers(
        self,
        elevation: List[List[float]],
        rng: random.Random,
        num_rivers: int = 4,
    ) -> None:
        """
        Carve rivers by walking downhill from high-elevation tiles
        toward water or the map edge.

        Visual generation only — no hydrology simulation.
        """
        # Find candidate source tiles: mountains or high-elevation grass/forest
        sources = []
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if elevation[y][x] > 0.58 and self.cells[y][x].biome != BiomeType.WATER:
                    sources.append((x, y))

        if not sources:
            return

        rng.shuffle(sources)
        rivers_carved = 0

        for sx, sy in sources:
            if rivers_carved >= num_rivers:
                break

            # Walk downhill
            path = []
            visited = set()
            cx, cy = sx, sy
            max_steps = self.width + self.height  # safety limit

            for _ in range(max_steps):
                if (cx, cy) in visited:
                    break
                visited.add((cx, cy))

                # Stop if we reached water or the edge
                if self.cells[cy][cx].biome == BiomeType.WATER:
                    break
                if cx <= 0 or cy <= 0 or cx >= self.width - 1 or cy >= self.height - 1:
                    path.append((cx, cy))
                    break

                path.append((cx, cy))

                # Find lowest elevation neighbor
                best_n = None
                best_e = elevation[cy][cx]
                neighbors = [
                    (cx - 1, cy), (cx + 1, cy),
                    (cx, cy - 1), (cx, cy + 1),
                ]
                # Add slight randomness so rivers aren't perfectly straight
                rng.shuffle(neighbors)

                for nx, ny in neighbors:
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited and elevation[ny][nx] <= best_e:
                            best_e = elevation[ny][nx]
                            best_n = (nx, ny)

                if best_n is None:
                    break  # stuck in a local minimum
                cx, cy = best_n

            # Only carve if river is at least 4 tiles long
            if len(path) >= 4:
                for rx, ry in path:
                    if self.cells[ry][rx].biome not in (BiomeType.WATER, BiomeType.MOUNTAIN):
                        self.cells[ry][rx].biome = BiomeType.WATER
                rivers_carved += 1

    # ------------------------------------------------------------------
    # Access helpers
    # ------------------------------------------------------------------

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        raise IndexError(
            f"Cell ({x}, {y}) is out of bounds for "
            f"{self.width}x{self.height} grid"
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

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
            "resources": [r.to_dict() for r in self.resources],
        }
