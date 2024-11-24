from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class DynamicObstacle:
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    radius: float
    lifetime: Optional[float] = None

    def update(self, dt: float):
        """Update obstacle position based on velocity"""
        x, y = self.position
        vx, vy = self.velocity
        self.position = (x + vx * dt, y + vy * dt)

        # Bounce off boundaries
        if not (0 <= x <= 49):
            self.velocity = (-vx, vy)
        if not (0 <= y <= 49):
            self.velocity = (vx, -vy)

    def affects_position(self, pos: Tuple[int, int], buffer: float = 1.0) -> bool:
        """Check if the obstacle affects a given position"""
        dx = pos[0] - self.position[0]
        dy = pos[1] - self.position[1]
        return (dx * dx + dy * dy) <= (self.radius + buffer) ** 2