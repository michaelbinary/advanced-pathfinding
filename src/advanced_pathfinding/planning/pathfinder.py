from typing import List, Tuple, Dict, Optional
import heapq
import asyncio
from rich.console import Console
import os
from ..core.grid import GridCell, initialize_grid
from ..core.agents import Agent
from ..core.obstacles import DynamicObstacle
from .traffic import TrafficManager
from ..visualization.analysis import SimulationAnalyzer
from ..visualization.renderer import SimulationRenderer

console = Console()


class AdvancedPathPlanner:
    def __init__(self, grid_size: Tuple[int, int], seed: int = None):
        self.grid_size = grid_size
        self.grid = initialize_grid(grid_size, seed)
        self.dynamic_obstacles: List[DynamicObstacle] = []
        self.agents: Dict[str, Agent] = {}
        self.traffic_manager = TrafficManager()
        self.simulation_time = 0.0
        self.paths_history = []
        # Initialize analyzer and renderer
        self.analyzer = SimulationAnalyzer(grid_size)
        self.renderer = SimulationRenderer(grid_size)

    async def find_path(self, start: Tuple[int, int], goal: Tuple[int, int],
                        constraints: Dict[str, float]) -> Optional[List[Tuple[int, int]]]:
        def heuristic(pos: Tuple[int, int]) -> float:
            return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5

        open_set = [(0, start)]
        heapq.heapify(open_set)

        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if not (0 <= neighbor[0] < self.grid_size[0] and
                        0 <= neighbor[1] < self.grid_size[1]):
                    continue

                cell = self.grid[neighbor[0]][neighbor[1]]
                move_cost = cell.traversal_cost(self.simulation_time)

                if dx != 0 and dy != 0:
                    move_cost *= 1.4142

                if move_cost > constraints.get('max_cost', float('inf')):
                    continue

                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def add_dynamic_obstacle(self, obstacle: DynamicObstacle):
        self.dynamic_obstacles.append(obstacle)

    def add_agent(self, agent: Agent):
        self.agents[agent.id] = agent

    async def update(self, dt: float):
        self.simulation_time += dt

        for obstacle in self.dynamic_obstacles:
            obstacle.update(dt)

        tasks = []
        for agent in self.agents.values():
            if agent.status == "active":
                if self._check_path_blocked(agent):
                    task = asyncio.create_task(self._replan_path(agent))
                    tasks.append(task)

                agent.update_position(dt)
                current_pos = (int(agent.position[0]), int(agent.position[1]))
                self.traffic_manager.update_congestion(current_pos)

        if tasks:
            await asyncio.gather(*tasks)

    def _check_path_blocked(self, agent: Agent) -> bool:
        if not agent.path:
            return False
        next_pos = agent.path[0]
        return any(obs.affects_position(next_pos) for obs in self.dynamic_obstacles)

    async def _replan_path(self, agent: Agent):
        current_pos = (int(agent.position[0]), int(agent.position[1]))
        new_path = await self.find_path(current_pos, agent.goal, agent.constraints)
        if new_path:
            agent.path = new_path

    async def simulate(self, duration: float, dt: float = 0.1):
        steps = int(duration / dt)
        frames = []
        for _ in range(steps):
            await self.update(dt)
            frames.append(self._get_simulation_state())
        return frames

    def _get_simulation_state(self):
        return {
            'time': self.simulation_time,
            'obstacles': self.dynamic_obstacles,
            'agents': self.agents,
            'congestion': dict(self.traffic_manager.congestion)
        }

    def save_analysis(self, output_dir: str = "simulation_results") -> str:
        """Save comprehensive analysis of the simulation"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        return self.analyzer.save_analysis(
            output_dir=output_dir,
            agents=self.agents,
            traffic_manager=self.traffic_manager,
            simulation_time=self.simulation_time
        )

    def visualize_realtime(self, frames, output_path=None):
        """
        Visualize the simulation and optionally save as GIF

        Args:
            frames: List of simulation frames
            output_path: Optional path to save the animation as GIF
        """
        self.renderer.create_animation(frames, self.grid, output_path=output_path)