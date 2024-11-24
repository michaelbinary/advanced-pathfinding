import pytest
import asyncio
from advanced_pathfinding import AdvancedPathPlanner, Agent
from advanced_pathfinding.core.obstacles import DynamicObstacle

pytestmark = pytest.mark.asyncio  # Mark all tests in this file as async


async def test_basic_pathfinding():
    # Initialize planner with a small grid
    planner = AdvancedPathPlanner((10, 10), seed=42)

    # Create a simple agent
    agent = Agent(
        id="test_agent",
        start=(0, 0),
        goal=(9, 9),
        speed=1.0,
        position=(0, 0),
        path=[],
        constraints={'max_cost': 20}
    )

    # Add agent and find path
    planner.add_agent(agent)
    path = await planner.find_path(agent.start, agent.goal, agent.constraints)

    # Verify path exists and is valid
    assert path is not None
    assert len(path) > 0
    assert path[0] == agent.start
    assert path[-1] == agent.goal

    # Verify path continuity
    for i in range(len(path) - 1):
        dx = abs(path[i][0] - path[i + 1][0])
        dy = abs(path[i][1] - path[i + 1][1])
        assert dx <= 1 and dy <= 1  # Ensure moves are adjacent


async def test_obstacle_avoidance():
    planner = AdvancedPathPlanner((10, 10), seed=42)

    # Create agent and path
    agent = Agent(
        id="test_agent",
        start=(0, 0),
        goal=(9, 9),
        speed=1.0,
        position=(0, 0),
        path=[],
        constraints={'max_cost': 20}
    )

    planner.add_agent(agent)
    initial_path = await planner.find_path(agent.start, agent.goal, agent.constraints)
    agent.path = initial_path

    # Add obstacle in path
    obstacle = DynamicObstacle("obs1", (5, 5), (0, 0), 1.0)
    planner.add_dynamic_obstacle(obstacle)

    # Update and verify path changes
    await planner.update(0.1)
    assert agent.path != initial_path  # Path should be replanned


async def test_simulation():
    planner = AdvancedPathPlanner((10, 10), seed=42)

    # Add agent
    agent = Agent(
        id="test_agent",
        start=(0, 0),
        goal=(9, 9),
        speed=1.0,
        position=(0, 0),
        path=[],
        constraints={'max_cost': 20}
    )

    planner.add_agent(agent)
    path = await planner.find_path(agent.start, agent.goal, agent.constraints)
    agent.path = path

    # Run simulation
    frames = await planner.simulate(duration=5.0, dt=0.1)

    # Verify simulation output
    assert len(frames) > 0
    assert all(isinstance(frame, dict) for frame in frames)
    assert all('time' in frame for frame in frames)
    assert all('agents' in frame for frame in frames)


# Add more specific test cases
async def test_path_with_terrain():
    planner = AdvancedPathPlanner((10, 10), seed=42)

    agent = Agent(
        id="terrain_test",
        start=(0, 0),
        goal=(9, 9),
        speed=1.0,
        position=(0, 0),
        path=[],
        constraints={'max_cost': 30}  # Higher cost to allow for terrain
    )

    planner.add_agent(agent)
    path = await planner.find_path(agent.start, agent.goal, agent.constraints)

    assert path is not None
    # Path should exist despite terrain costs


async def test_multiple_agents():
    planner = AdvancedPathPlanner((10, 10), seed=42)

    agents = [
        Agent(
            id=f"agent_{i}",
            start=(0, i),
            goal=(9, i),
            speed=1.0,
            position=(0, i),
            path=[],
            constraints={'max_cost': 20}
        ) for i in range(3)
    ]

    for agent in agents:
        planner.add_agent(agent)
        path = await planner.find_path(agent.start, agent.goal, agent.constraints)
        agent.path = path
        assert path is not None

    # Run a short simulation
    frames = await planner.simulate(duration=1.0, dt=0.1)
    assert len(frames) == 10  # Should have 10 frames for 1.0 duration with 0.1 dt


if __name__ == '__main__':
    pytest.main(['-v', __file__])