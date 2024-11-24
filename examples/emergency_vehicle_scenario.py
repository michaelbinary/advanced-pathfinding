import asyncio
from advanced_pathfinding import AdvancedPathPlanner
from advanced_pathfinding.core.agents import Agent
from advanced_pathfinding.core.obstacles import DynamicObstacle
from rich.console import Console
import os

console = Console()

SCENARIO_NAME = "emergency_vehicle"


async def setup_environment():
    """Initialize planner and create output directories"""
    # Initialize planner with a larger grid for urban environment
    planner = AdvancedPathPlanner((100, 100), seed=42)

    # Create output directories
    base_dir = os.path.dirname(__file__)
    output_dirs = {
        'analysis': os.path.join(base_dir, 'simulation_results', SCENARIO_NAME),
        'gifs': os.path.join(base_dir, 'simulation_gifs')
    }

    for dir_path in output_dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    return planner, output_dirs


async def create_regular_vehicles(num_vehicles=10):
    """Create regular traffic vehicles"""
    return [
        Agent(
            id=f"vehicle_{i}",
            start=(0 + i * 5, 0),
            goal=(90, 90),
            speed=1.0,  # Regular speed
            position=(0 + i * 5, 0),
            path=[],
            constraints={'max_cost': 15, 'priority': 1},  # Low priority
        ) for i in range(num_vehicles)
    ]


def create_emergency_vehicle():
    """Create emergency vehicle with high priority"""
    return Agent(
        id="ambulance_1",
        start=(0, 0),
        goal=(90, 90),
        speed=2.0,  # Double speed
        position=(0, 0),
        path=[],
        constraints={'max_cost': 30, 'priority': 5},  # High priority
    )


def create_obstacles():
    """Create static obstacles representing road blockages"""
    return [
        DynamicObstacle("roadblock_1", (40, 40), (0, 0), 3.0),  # Stationary obstacle
        DynamicObstacle("roadblock_2", (60, 60), (0, 0), 2.0),
        DynamicObstacle("roadblock_3", (20, 80), (0, 0), 2.5),
    ]


async def initialize_vehicles(planner, vehicles):
    """Initialize vehicles with paths"""
    for vehicle in vehicles:
        planner.add_agent(vehicle)
        path = await planner.find_path(vehicle.start, vehicle.goal, vehicle.constraints)
        if path:
            vehicle.path = path
            console.print(f"[green]Path found for {vehicle.id}[/green]")
        else:
            console.print(f"[red]No path found for {vehicle.id}[/red]")


async def main():
    # Setup
    planner, output_dirs = await setup_environment()

    # Create and initialize regular vehicles
    console.print("[bold blue]Initializing regular vehicles...[/bold blue]")
    regular_vehicles = await create_regular_vehicles()
    await initialize_vehicles(planner, regular_vehicles)

    # Add obstacles
    obstacles = create_obstacles()
    for obstacle in obstacles:
        planner.add_dynamic_obstacle(obstacle)

    # Add emergency vehicle
    console.print("[bold yellow]Emergency vehicle entering the scene...[/bold yellow]")
    emergency_vehicle = create_emergency_vehicle()
    planner.add_agent(emergency_vehicle)
    path = await planner.find_path(emergency_vehicle.start, emergency_vehicle.goal,
                                   emergency_vehicle.constraints)
    if path:
        emergency_vehicle.path = path
        console.print(f"[green]Path found for emergency vehicle[/green]")
    else:
        console.print(f"[red]No path found for emergency vehicle[/red]")

    # Run simulation
    console.print("[bold blue]Starting simulation...[/bold blue]")
    frames = await planner.simulate(duration=60.0)  # Longer simulation to see full paths

    # Save analysis and create visualization
    analysis_dir = planner.save_analysis(output_dir=output_dirs['analysis'])
    console.print(f"[green]Analysis saved to: {analysis_dir}[/green]")

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