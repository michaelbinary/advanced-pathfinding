import asyncio
from advanced_pathfinding import AdvancedPathPlanner
from advanced_pathfinding.core.agents import Agent
from advanced_pathfinding.core.obstacles import DynamicObstacle
from rich.console import Console
import os
import random

console = Console()

SCENARIO_NAME = "dense_traffic"


async def setup_environment():
    """Initialize planner and create output directories"""
    planner = AdvancedPathPlanner((80, 80), seed=42)

    base_dir = os.path.dirname(__file__)
    output_dirs = {
        'analysis': os.path.join(base_dir, 'simulation_results', SCENARIO_NAME),
        'gifs': os.path.join(base_dir, 'simulation_gifs')
    }

    for dir_path in output_dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    return planner, output_dirs


def create_rush_hour_vehicles(num_vehicles=40):
    """Create vehicles for rush hour scenario"""
    vehicles = []
    business_district_center = (60, 60)
    residential_areas = [(10, 10), (10, 30), (30, 10), (20, 20)]

    for i in range(num_vehicles):
        start = random.choice(residential_areas)
        goal = (
            business_district_center[0] + random.randint(-10, 10),
            business_district_center[1] + random.randint(-10, 10)
        )

        vehicle = Agent(
            id=f"vehicle_{i}",
            start=start,
            goal=goal,
            speed=random.uniform(0.8, 1.2),
            position=start,
            path=[],
            constraints={
                'max_cost': 20,
                'priority': 1
            }
        )
        vehicles.append(vehicle)

    return vehicles


def create_construction_sites():
    """Create static obstacles representing construction"""
    return [
        DynamicObstacle("construction_1", (30, 30), (0, 0), 2.0),
        DynamicObstacle("construction_2", (45, 45), (0, 0), 2.0),
        DynamicObstacle("construction_3", (40, 60), (0, 0), 1.5),
    ]


async def initialize_vehicles(planner, vehicles):
    """Initialize vehicles with paths"""
    for i, vehicle in enumerate(vehicles):
        planner.add_agent(vehicle)
        path = await planner.find_path(vehicle.start, vehicle.goal, vehicle.constraints)
        if path:
            vehicle.path = path
            console.print(f"[green]Path found for {vehicle.id}[/green]")
        else:
            console.print(f"[red]No path found for {vehicle.id}[/red]")

        # Add small delay between vehicle initializations
        if i % 5 == 0:
            await asyncio.sleep(0.1)


def analyze_traffic(planner):
    """Analyze traffic patterns and congestion"""
    congestion_points = [pos for pos, level in planner.traffic_manager.congestion.items()
                         if level > 5]

    console.print("\n[bold yellow]Traffic Analysis:[/bold yellow]")
    console.print(f"Number of high congestion points: {len(congestion_points)}")

    if congestion_points:
        most_congested = max(planner.traffic_manager.congestion.items(),
                             key=lambda x: x[1])
        console.print(f"Most congested point: {most_congested[0]} "
                      f"with level {most_congested[1]}")

    return len(congestion_points)


async def main():
    # Setup
    planner, output_dirs = await setup_environment()

    # Create and initialize vehicles
    console.print("[bold blue]Initializing vehicles for rush hour...[/bold blue]")
    vehicles = create_rush_hour_vehicles()

    # Add construction sites
    obstacles = create_construction_sites()
    for obstacle in obstacles:
        planner.add_dynamic_obstacle(obstacle)

    # Initialize vehicles
    await initialize_vehicles(planner, vehicles)

    # Run simulation
    console.print("[bold blue]Starting rush hour simulation...[/bold blue]")
    frames = await planner.simulate(duration=90.0)

    # Save analysis and create visualization
    analysis_dir = planner.save_analysis(output_dir=output_dirs['analysis'])
    console.print(f"[green]Analysis saved to: {analysis_dir}[/green]")

    # Analyze traffic patterns
    congestion_count = analyze_traffic(planner)

    # Save and show visualization
    gif_path = os.path.join(output_dirs['gifs'],
                            f'{SCENARIO_NAME}_simulation_{congestion_count}_congestion_points.gif')
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