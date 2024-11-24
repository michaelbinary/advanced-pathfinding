import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple

class SimulationAnalyzer:
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size

    def save_analysis(self, output_dir: str, agents: Dict, traffic_manager, simulation_time: float) -> str:
        """Save comprehensive analysis of the simulation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_dir = os.path.join(output_dir, f"analysis_{timestamp}")
        os.makedirs(analysis_dir, exist_ok=True)

        # Save configuration
        config = {
            "grid_size": self.grid_size,
            "num_agents": len(agents),
            "simulation_time": simulation_time
        }
        with open(os.path.join(analysis_dir, "config.json"), 'w') as f:
            json.dump(config, f, indent=2)

        # Generate agent statistics
        agent_stats = self._generate_agent_stats(agents)
        with open(os.path.join(analysis_dir, "agent_stats.json"), 'w') as f:
            json.dump(agent_stats, f, indent=2)

        # Generate plots
        self._generate_analysis_plots(analysis_dir, agent_stats, traffic_manager)

        return analysis_dir

    def _generate_agent_stats(self, agents: Dict) -> List[Dict]:
        agent_stats = []
        for agent_id, agent in agents.items():
            metrics = agent.calculate_path_metrics() if hasattr(agent, 'calculate_path_metrics') else {}
            agent_stats.append({
                "id": agent_id,
                "status": agent.status,
                "distance_traveled": metrics.get("distance", 0),
                "optimal_distance": metrics.get("optimal_distance", 0),
                "path_efficiency": metrics.get("efficiency", 0),
                "average_speed": agent.speed,
                "constraints": agent.constraints
            })
        return agent_stats

    def _generate_analysis_plots(self, analysis_dir: str, agent_stats: List[Dict], traffic_manager):
        # Path Efficiency Plot
        plt.figure(figsize=(10, 6))
        efficiencies = [stat['path_efficiency'] for stat in agent_stats]
        plt.bar(range(len(efficiencies)), efficiencies)
        plt.xlabel('Agent ID')
        plt.ylabel('Path Efficiency')
        plt.title('Path Efficiency by Agent')
        plt.xticks(range(len(efficiencies)), [stat['id'] for stat in agent_stats], rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, 'path_efficiency.png'))
        plt.close()

        # Distance Comparison Plot
        plt.figure(figsize=(10, 6))
        actual_distances = [stat['distance_traveled'] for stat in agent_stats]
        optimal_distances = [stat['optimal_distance'] for stat in agent_stats]
        x = range(len(actual_distances))
        plt.bar(x, actual_distances, alpha=0.5, label='Actual Distance')
        plt.bar(x, optimal_distances, alpha=0.5, label='Optimal Distance')
        plt.xlabel('Agent ID')
        plt.ylabel('Distance')
        plt.title('Actual vs Optimal Distance by Agent')
        plt.legend()
        plt.xticks(x, [stat['id'] for stat in agent_stats], rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, 'distance_comparison.png'))
        plt.close()

        # Congestion Heatmap
        plt.figure(figsize=(10, 10))
        congestion_map = np.zeros(self.grid_size)
        if hasattr(traffic_manager, 'congestion'):
            for pos, level in traffic_manager.congestion.items():
                if 0 <= pos[0] < self.grid_size[0] and 0 <= pos[1] < self.grid_size[1]:
                    congestion_map[pos[0], pos[1]] = level
        plt.imshow(congestion_map, cmap='YlOrRd')
        plt.colorbar(label='Congestion Level')
        plt.title('Congestion Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, 'congestion_heatmap.png'))
        plt.close()