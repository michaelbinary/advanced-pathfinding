import asyncio
from advanced_pathfinding import AdvancedPathPlanner
from advanced_pathfinding.core.agents import Agent
from advanced_pathfinding.core.obstacles import DynamicObstacle
from rich.console import Console
import os

console = Console()


async def main():
    # Initialize planner
    planner = AdvancedPathPlanner((50, 50), seed=42)

    # Create dynamic obstacles
    obstacles = [
        DynamicObstacle("obs1", (10, 10), (0.5, 0.3), 1.5),
        DynamicObstacle("obs2", (30, 30), (-0.3, 0.4), 2.0),
        DynamicObstacle("obs3", (20, 40), (0.4, -0.3), 1.0),
    ]

    for obs in obstacles:
        planner.add_dynamic_obstacle(obs)

    # Create diverse agents
    agents = [
        Agent(
            "agent1",
            start=(0, 0),
            goal=(45, 45),
            speed=1.5,
            position=(0, 0),
            path=[],
            constraints={'max_cost': 20, 'priority': 3},
        ),
        Agent(
            "emergency1",
            start=(0, 25),
            goal=(49, 25),
            speed=2.0,
            position=(0, 25),
            path=[],
            constraints={'max_cost': 30, 'priority': 5},
        )
    ]

    # Initialize agents with paths
    console.print("[bold blue]Initializing agents...[/bold blue]")
    for agent in agents:
        planner.add_agent(agent)
        path = await planner.find_path(agent.start, agent.goal, agent.constraints)
        if path:
            agent.path = path
            console.print(f"[green]Path found for {agent.id}[/green]")
        else:
            console.print(f"[red]No path found for {agent.id}[/red]")

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'simulation_results')
    os.makedirs(output_dir, exist_ok=True)

    # Run simulation
    console.print("[bold blue]Starting simulation...[/bold blue]")
    frames = await planner.simulate(duration=30.0)

    # Save analysis and visualize
    analysis_dir = planner.save_analysis(output_dir=output_dir)
    console.print(f"[green]Analysis saved to: {analysis_dir}[/green]")

    planner.visualize_realtime(frames)


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