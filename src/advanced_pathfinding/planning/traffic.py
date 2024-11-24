from collections import defaultdict
from typing import List, Tuple, Dict

class TrafficManager:
    def __init__(self):
        self.congestion = defaultdict(int)
        self.reserved_paths = defaultdict(list)  # time -> [(agent_id, position)]

    def update_congestion(self, pos: Tuple[int, int]):
        """Update congestion level at a given position"""
        self.congestion[pos] += 1

    def get_congestion_cost(self, pos: Tuple[int, int]) -> float:
        """Get the congestion cost for a given position"""
        return self.congestion[pos] * 0.2

    def reserve_path(self, agent_id: str, path: List[Tuple[int, int]], time_windows: List[float]):
        """Reserve a path for an agent at specific time windows"""
        for t, pos in zip(time_windows, path):
            self.reserved_paths[t].append((agent_id, pos))

    def check_collision(self, pos: Tuple[int, int], time: float) -> bool:
        """Check if there's a collision at a given position and time"""
        window = int(time * 10) / 10  # Round to nearest 0.1
        return any(p == pos for _, p in self.reserved_paths[window])

    def get_congestion_map(self, grid_size: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
        """Get the current congestion map"""
        return dict(self.congestion)