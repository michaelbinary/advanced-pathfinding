# Quick Start Guide

## Basic Usage

Here's a simple example to get you started with Advanced Pathfinding:

```python
import asyncio
from advanced_pathfinding import AdvancedPathPlanner, Agent

async def main():
    # Initialize the pathfinding system
    planner = AdvancedPathPlanner((50, 50))  # Create a 50x50 grid
    
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
    
    # Visualize results
    planner.visualize_realtime(frames)

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

### 1. Grid System
- The environment is represented as a grid
- Each cell has different terrain types affecting movement cost
- Terrain types include: URBAN, HIGHWAY, RESIDENTIAL, PARK, CONSTRUCTION, RESTRICTED

### 2. Agents
- Agents navigate from start to goal positions
- Each agent has customizable speed and constraints
- Agents automatically avoid obstacles and other agents

### 3. Dynamic Obstacles
```python
from advanced_pathfinding import DynamicObstacle

obstacle = DynamicObstacle(
    id="obs1",
    position=(10, 10),
    velocity=(0.5, 0.3),
    radius=1.5
)
planner.add_dynamic_obstacle(obstacle)
```

### 4. Path Planning
- A* algorithm with dynamic cost calculations
- Considers terrain, obstacles, and congestion
- Automatic path replanning when blocked

## Common Scenarios

### 1. Emergency Vehicle Routing
```python
emergency_vehicle = Agent(
    id="emergency1",
    start=(0, 0),
    goal=(49, 49),
    speed=2.0,  # Faster speed
    position=(0, 0),
    path=[],
    constraints={'max_cost': 30, 'priority': 5}  # Higher priority
)
```

### 2. Multi-Agent Coordination
```python
# Create multiple agents
agents = [
    Agent(id="agent1", start=(0, 0), goal=(45, 45), ...),
    Agent(id="agent2", start=(0, 45), goal=(45, 0), ...),
    Agent(id="agent3", start=(25, 0), goal=(25, 45), ...)
]

# Add all agents
for agent in agents:
    planner.add_agent(agent)
    path = await planner.find_path(agent.start, agent.goal, agent.constraints)
    agent.path = path
```

## Analysis and Visualization

### 1. Save Analysis Results
```python
analysis_dir = planner.save_analysis()
print(f"Analysis saved to: {analysis_dir}")
```

### 2. Customize Visualization
```python
from advanced_pathfinding.visualization.renderer import SimulationRenderer

renderer = SimulationRenderer(grid_size=(50, 50))
renderer.create_animation(frames, planner.grid, output_path="simulation.gif")
```

## Next Steps

- Check out [Advanced Usage](advanced_usage.md) for more features
- See [API Reference](api_reference.md) for detailed documentation
- Visit our [Examples](../examples/) directory for more scenarios