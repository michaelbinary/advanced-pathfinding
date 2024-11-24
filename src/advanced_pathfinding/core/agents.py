from dataclasses import dataclass
from typing import Tuple, List, Dict


@dataclass
class Agent:
    id: str
    start: Tuple[int, int]
    goal: Tuple[int, int]
    speed: float
    position: Tuple[float, float]
    path: List[Tuple[int, int]]
    constraints: Dict[str, float]
    status: str = "active"  # active, waiting, finished
    priority: int = 1

    def update_position(self, dt: float):
        """Update agent's position based on current path and speed"""
        if not self.path or self.status != "active":
            return

        target = self.path[0]
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < 0.1:  # Reached waypoint
            self.position = target
            self.path.pop(0)
            if not self.path:
                self.status = "finished"
            return

        # Move towards target
        speed = self.speed * dt
        if distance > speed:
            self.position = (
                self.position[0] + dx * speed / distance,
                self.position[1] + dy * speed / distance
            )

    def calculate_path_metrics(self) -> Dict[str, float]:
        """Calculate metrics for the agent's current path"""
        if not self.path:
            return {
                "distance": 0,
                "optimal_distance": 0,
                "efficiency": 0
            }

        actual_distance = sum(
            ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            for p1, p2 in zip(self.path[:-1], self.path[1:])
        )
        optimal_distance = ((self.start[0] - self.goal[0]) ** 2 +
                            (self.start[1] - self.goal[1]) ** 2) ** 0.5

        efficiency = optimal_distance / actual_distance if actual_distance > 0 else 0

        return {
            "distance": actual_distance,
            "optimal_distance": optimal_distance,
            "efficiency": efficiency
        }