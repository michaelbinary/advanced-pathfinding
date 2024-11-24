import asyncio
from advanced_pathfinding import AdvancedPathPlanner
from advanced_pathfinding.core.agents import Agent
from advanced_pathfinding.core.obstacles import DynamicObstacle
from rich.console import Console
import os
import math

console = Console()

SCENARIO_NAME = "dynamic_obstacles"


async def setup_environment():
    """Initialize planner and create output directories"""
    planner = AdvancedPathPlanner((70, 70), seed=42)

    base_dir = os.path.dirname(__file__)
    output_dirs = {
        'analysis': os.path.join(base_dir, 'simulation_results', SCENARIO_NAME),
        'gifs': os.path.join(base_dir, 'simulation_gifs')
    }

    for dir_path in output_dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    return planner, output_dirs


def create_patrol_obstacles():
    """Create obstacles with different movement patterns"""
    return [
        # Circular moving obstacle
        DynamicObstacle(
            "patrol_1",
            (35, 35),
            (math.cos(0) * 0.5, math.sin(0) * 0.5),
            2.0
        ),
        # Horizontal patrol
        DynamicObstacle("patrol_2", (20, 40), (0.8, 0), 1.5),
        # Vertical patrol
        DynamicObstacle("patrol_3", (40, 20), (0, 0.8), 1.5),
    ]


def create_test_agents():
    """Create agents to test obstacle avoidance"""
    return [
        Agent(
            "agent_1",
            start=(10, 40),
            goal=(60, 40),
            speed=1.2,
            position=(10, 40),
            path=[],
            constraints={'max_cost': 25, 'priority': 2},
        ),
        Agent(
            "agent_2",
            start=(40, 10),
            goal=(40, 60),
            speed=1.2,
            position=(40, 10),
            path=[],
            constraints={'max_cost': 25, 'priority': 2},
        ),
    ]


async def initialize_agents(planner, agents):
    """Initialize agents with paths"""
    replan_count = {agent.id: 0 for agent in agents}

    for agent in agents:
        planner.add_agent(agent)
        path = await planner.find_path(agent.start, agent.goal, agent.constraints)
        if path:
            agent.path = path
            console.print(f"[green]Path found for {agent.id}[/green]")
        else:
            console.print(f"[red]No path found for {agent.id}[/red]")

    return replan_count


async def track_replans(planner, agents, replan_count, duration):
    """Track path replanning events"""
    steps = int(duration / 0.1)  # Check every 0.1 seconds
    for _ in range(steps):
        for agent in agents:
            if planner._check_path_blocked(agent):
                replan_count[agent.id] += 1
        await asyncio.sleep(0.1)
    return replan_count


async def main():
    # Setup
    planner, output_dirs = await setup_environment()

    # Create and add obstacles
    obstacles = create_patrol_obstacles()
    for obstacle in obstacles:
        planner.add_dynamic_obstacle(obstacle)

    # Create and initialize agents
    console.print("[bold blue]Initializing agents...[/bold blue]")
    agents = create_test_agents()
    replan_count = await initialize_agents(planner, agents)

    # Run simulation
    console.print("[bold blue]Starting simulation with dynamic obstacles...[/bold blue]")
    simulation_duration = 30.0  # Shorter duration for testing

    # Run simulation and track replans concurrently
    tracking_task = asyncio.create_task(
        track_replans(planner, agents, replan_count, simulation_duration)
    )
    frames = await planner.simulate(duration=simulation_duration)
    replan_count = await tracking_task

    # Save analysis
    analysis_dir = planner.save_analysis(output_dir=output_dirs['analysis'])
    console.print(f"[green]Analysis saved to: {analysis_dir}[/green]")

    # Print replan statistics
    console.print("\n[bold yellow]Path Replanning Statistics:[/bold yellow]")
    for agent_id, count in replan_count.items():
        console.print(f"{agent_id}: Replanned {count} times")

    # Save and show visualization
    gif_path = os.path.join(output_dirs['gifs'], f'{SCENARIO_NAME}_simulation.gif')
    console.print(f"[blue]Saving simulation GIF to: {gif_path}[/blue]")
    planner.visualize_realtime(frames, output_path=gif_path)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[yellow]Simulation interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print_exception()
    finally:
        console.print("[blue]Simulation ended[/blue]")