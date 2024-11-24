from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from enum import Enum
import random
import numpy as np


class WeatherType(Enum):
    CLEAR = "clear"
    RAIN = "rain"
    SNOW = "snow"
    FOG = "fog"
    STORM = "storm"


@dataclass
class WeatherCondition:
    rain_intensity: float  # 0.0 to 1.0
    visibility: float  # 0.0 to 1.0 (1.0 being perfect visibility)
    wind_speed: float  # in m/s
    temperature: float  # in Celsius

    @classmethod
    def create_preset(cls, weather_type: WeatherType) -> 'WeatherCondition':
        """Create preset weather conditions based on weather type"""
        presets = {
            WeatherType.CLEAR: cls(
                rain_intensity=0.0,
                visibility=1.0,
                wind_speed=2.0,
                temperature=20.0
            ),
            WeatherType.RAIN: cls(
                rain_intensity=0.6,
                visibility=0.7,
                wind_speed=5.0,
                temperature=15.0
            ),
            WeatherType.SNOW: cls(
                rain_intensity=0.4,
                visibility=0.5,
                wind_speed=3.0,
                temperature=-2.0
            ),
            WeatherType.FOG: cls(
                rain_intensity=0.1,
                visibility=0.3,
                wind_speed=1.0,
                temperature=10.0
            ),
            WeatherType.STORM: cls(
                rain_intensity=0.9,
                visibility=0.2,
                wind_speed=15.0,
                temperature=18.0
            )
        }
        return presets[weather_type]

    def get_movement_multiplier(self) -> float:
        """Calculate how weather affects movement speed"""
        multiplier = 1.0

        # Rain effects
        multiplier *= 1.0 - (self.rain_intensity * 0.3)

        # Visibility effects
        multiplier *= 0.5 + (self.visibility * 0.5)

        # Wind effects
        if self.wind_speed > 10.0:
            multiplier *= 0.8

        # Temperature effects
        if self.temperature < 0:
            multiplier *= 0.7  # Ice/snow conditions
        elif self.temperature > 35:
            multiplier *= 0.9  # Extreme heat

        return max(0.2, multiplier)  # Ensure minimum 20% speed


class WeatherSystem:
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.current_conditions: Dict[Tuple[int, int], WeatherCondition] = {}
        self.global_condition: Optional[WeatherCondition] = None
        self._weather_noise = np.random.RandomState()

    def set_global_weather(self, condition: WeatherCondition):
        """Set a global weather condition"""
        self.global_condition = condition
        self.current_conditions.clear()

    def set_local_weather(self, position: Tuple[int, int], condition: WeatherCondition):
        """Set weather condition for a specific position"""
        self.current_conditions[position] = condition

    def get_weather_at(self, position: Tuple[int, int]) -> WeatherCondition:
        """Get weather condition at a specific position"""
        return self.current_conditions.get(position, self.global_condition)

    def update(self, dt: float):
        """Update weather conditions over time"""
        if self.global_condition:
            # Add some random variation to the global weather
            noise = self._generate_weather_noise()
            self.global_condition = WeatherCondition(
                rain_intensity=min(1.0, max(0.0, self.global_condition.rain_intensity + noise * 0.1)),
                visibility=min(1.0, max(0.1, self.global_condition.visibility + noise * 0.1)),
                wind_speed=max(0.0, self.global_condition.wind_speed + noise),
                temperature=self.global_condition.temperature + noise * 0.5
            )

        # Update local weather conditions
        for pos in list(self.current_conditions.keys()):
            if random.random() < 0.1:  # 10% chance to remove local weather effect
                del self.current_conditions[pos]

    def _generate_weather_noise(self) -> float:
        """Generate random weather variations"""
        return self._weather_noise.normal(0, 0.05)

    def create_weather_front(self,
                             start_position: Tuple[int, int],
                             condition: WeatherCondition,
                             radius: int):
        """Create a weather front centered at a position"""
        for x in range(max(0, start_position[0] - radius),
                       min(self.grid_size[0], start_position[0] + radius + 1)):
            for y in range(max(0, start_position[1] - radius),
                           min(self.grid_size[1], start_position[1] + radius + 1)):
                # Calculate distance from center
                distance = ((x - start_position[0]) ** 2 +
                            (y - start_position[1]) ** 2) ** 0.5

                if distance <= radius:
                    # Intensity decreases with distance from center
                    intensity = 1.0 - (distance / radius)
                    local_condition = WeatherCondition(
                        rain_intensity=condition.rain_intensity * intensity,
                        visibility=min(1.0, condition.visibility + (1 - intensity)),
                        wind_speed=condition.wind_speed * intensity,
                        temperature=condition.temperature
                    )
                    self.set_local_weather((x, y), local_condition)

    def save_weather_state(self) -> Dict:
        """Save current weather state for analysis"""
        return {
            'global_condition': self.global_condition,
            'local_conditions': self.current_conditions.copy(),
            'grid_size': self.grid_size
        }

    def load_weather_state(self, state: Dict):
        """Load a previously saved weather state"""
        self.global_condition = state['global_condition']
        self.current_conditions = state['local_conditions']
        self.grid_size = state['grid_size']


# Example usage in the pathfinding system:
"""
# In AdvancedPathPlanner.__init__:
self.weather_system = WeatherSystem(grid_size)
self.weather_system.set_global_weather(WeatherCondition.create_preset(WeatherType.CLEAR))

# In GridCell.traversal_cost:
weather = self.weather_system.get_weather_at((self.x, self.y))
weather_multiplier = weather.get_movement_multiplier()
return base_cost * weather_multiplier
"""