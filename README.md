# Advanced Grid-Based Pathfinding System

![Simulation Demo](simulation.gif)

A sophisticated multi-agent pathfinding system that simulates complex urban mobility scenarios with dynamic obstacles, terrain types, traffic management, and weather conditions. Perfect for robotics navigation, game AI, urban planning, and traffic simulation research.

## 🌟 Key Features

### Core Functionality
- **Multi-Agent Pathfinding**: Coordinate multiple agents with different priorities and constraints
- **Dynamic Obstacle Avoidance**: Real-time path replanning around moving obstacles
- **Terrain-Aware Routing**: Various terrain types affecting movement costs (urban, highway, residential, parks)
- **Traffic Management**: Congestion detection and avoidance
- **Weather Impact**: Simulates weather effects on movement and pathfinding

### Advanced Features
- **Priority-Based Routing**: Emergency vehicle prioritization
- **Congestion Analysis**: Real-time traffic density monitoring
- **Path Efficiency Metrics**: Detailed analysis of path optimality
- **Asynchronous Processing**: Efficient handling of multiple agents
- **Visualizations**: Real-time simulation rendering and analysis plots

## 🚀 Quick Start

```python
import asyncio
from advanced_pathfinding import AdvancedPathPlanner
from advanced_pathfinding.core.agents import Agent

async def main():
    # Initialize planner
    planner = AdvancedPathPlanner((50, 50))
    
    # Create an agent
    agent = Agent(
        id="agent1",
        start=(0, 0),
        goal=(45, 45),
        speed=1.5,
        position=(0, 0),
        path=[],
        constraints={'max_cost': 20}
    )
    
    # Add agent and find path
    planner.add_agent(agent)
    path = await planner.find_path(agent.start, agent.goal, agent.constraints)
    agent.path = path
    
    # Run simulation
    frames = await planner.simulate(duration=30.0)
    planner.visualize_realtime(frames)

if __name__ == "__main__":
    asyncio.run(main())
```

## 📊 Example Scenarios

### 1. Emergency Vehicle Routing
Demonstrates priority-based routing for emergency vehicles through congested areas.
```python
examples/emergency_vehicle_scenario.py
```

### 2. Dense Traffic Simulation
Simulates rush hour traffic with multiple agents and congestion analysis.
```python
examples/dense_traffic_scenario.py
```

### 3. Dynamic Obstacle Avoidance
Shows real-time path replanning around moving obstacles.
```python
examples/dynamic_obstacles_scenario.py
```

## 🛠 Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📋 Requirements

- Python 3.8+
- NumPy
- Matplotlib
- Rich (for CLI interface)
- Asyncio

## 🔍 Project Structure

```
advanced_pathfinding/
├── core/
│   ├── agents.py          # Agent definitions and behaviors
│   ├── grid.py           # Grid system and terrain types
│   ├── obstacles.py      # Dynamic obstacle implementation
│   └── weather.py        # Weather system and effects
├── planning/
│   ├── pathfinder.py     # Main pathfinding algorithm
│   └── traffic.py        # Traffic management system
└── visualization/
    ├── renderer.py       # Real-time visualization
    └── analysis.py       # Statistical analysis and plotting
```

## 📈 Analysis Features

- Path efficiency metrics
- Congestion heatmaps
- Traffic flow analysis
- Agent performance statistics
- Automated report generation

## 🎮 Usage Examples

### Basic Agent Movement
```python
agent = Agent(
    id="agent1",
    start=(0, 0),
    goal=(45, 45),
    speed=1.5,
    position=(0, 0),
    path=[],
    constraints={'max_cost': 20}
)
```

### Adding Dynamic Obstacles
```python
obstacle = DynamicObstacle(
    id="obs1",
    position=(10, 10),
    velocity=(0.5, 0.3),
    radius=1.5
)
planner.add_dynamic_obstacle(obstacle)
```

### Analyzing Results
```python
analysis_dir = planner.save_analysis()
print(f"Analysis saved to: {analysis_dir}")
```



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 📧 Contact

Michael La Rosa - hello@mlarosa.dev
