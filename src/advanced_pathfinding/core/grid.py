from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import random
import numpy as np

class TerrainType(Enum):
    URBAN = 1.2  # City streets
    HIGHWAY = 0.8  # Fast routes
    RESIDENTIAL = 1.5
    PARK = 1.3
    CONSTRUCTION = 2.5
    RESTRICTED = 10.0

    @classmethod
    def get_color(cls, terrain_type):
        return {
            cls.URBAN: '#A0A0A0',  # Gray
            cls.HIGHWAY: '#404040',  # Dark Gray
            cls.RESIDENTIAL: '#C0C0C0',  # Light Gray
            cls.PARK: '#90EE90',  # Light Green
            cls.CONSTRUCTION: '#FFA500',  # Orange
            cls.RESTRICTED: '#FF0000'  # Red
        }[terrain_type]

@dataclass
class WeatherCondition:
    rain_intensity: float
    visibility: float
    wind_speed: float
    temperature: float

class GridCell:
    def __init__(self, x: int, y: int, terrain: TerrainType):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.elevation = 0.0
        self.dynamic_obstacles: List['DynamicObstacle'] = []
        self.weather: Optional[WeatherCondition] = None
        self.risk_factor = 0.0
        self.congestion = 0

    def traversal_cost(self, time: float) -> float:
        base_cost = self.terrain.value
        elevation_cost = max(0, self.elevation * 0.1)

        weather_cost = 0
        if self.weather:
            weather_cost += self.weather.rain_intensity * 2
            weather_cost += (1 - self.weather.visibility) * 3
            weather_cost += max(0, (self.weather.wind_speed - 10) * 0.5)

        congestion_cost = self.congestion * 0.2
        risk_cost = self.risk_factor * 5

        return base_cost + elevation_cost + weather_cost + congestion_cost + risk_cost

def initialize_grid(grid_size, seed=None):
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    grid = []
    for x in range(grid_size[0]):
        row = []
        for y in range(grid_size[1]):
            if _is_highway(x, y):
                terrain = TerrainType.HIGHWAY
            elif _is_park(x, y):
                terrain = TerrainType.PARK
            elif _is_restricted(x, y):
                terrain = TerrainType.RESTRICTED
            elif random.random() < 0.1:
                terrain = TerrainType.CONSTRUCTION
            else:
                terrain = TerrainType.URBAN if random.random() < 0.7 else TerrainType.RESIDENTIAL

            cell = GridCell(x, y, terrain)
            cell.elevation = _generate_elevation(x, y)
            row.append(cell)
        grid.append(row)
    return grid

def _is_highway(x: int, y: int) -> bool:
    return (x % 10 == 0) or (y % 10 == 0)

def _is_park(x: int, y: int) -> bool:
    return (15 <= x <= 25 and 15 <= y <= 25) and random.random() < 0.7

def _is_restricted(x: int, y: int) -> bool:
    return ((x - 40) ** 2 + (y - 40) ** 2 < 25) and random.random() < 0.8

def _generate_elevation(x: int, y: int) -> float:
    base = np.sin(x / 10) * np.cos(y / 10)
    noise = np.random.normal(0, 0.1)
    return base + noise