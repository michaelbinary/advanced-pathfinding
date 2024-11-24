# API Reference

## Core Components

### AdvancedPathPlanner

```python
class AdvancedPathPlanner(grid_size: Tuple[int, int], seed: Optional[int] = None)
```

Main class for pathfinding and simulation.

#### Methods:

##### `async find_path(start: Tuple[int, int], goal: Tuple[int, int], constraints: Dict[str, float]) -> Optional[List[Tuple[int, int]]]`
Finds optimal path between start and goal positions.
- **Parameters:**
  - start: Starting coordinates (x, y)
  - goal: Goal coordinates (x, y)
  - constraints: Dictionary of constraints ('max_cost', 'priority')
- **Returns:** List of coordinates representing the path, or None if no path found

##### `add_agent(agent: Agent) -> None`
Adds an agent to the simulation.

##### `add_dynamic_obstacle(obstacle: DynamicObstacle) -> None`
Adds a dynamic obstacle to the simulation.

##### `async simulate(duration: float, dt: float = 0.1) -> List[Dict]`
Runs the simulation for specified duration.
- **Parameters:**
  - duration: Simulation duration in seconds
  - dt: Time step size
- **Returns:** List of simulation frames

### Agent

```python
@dataclass
class Agent:
    id: str
    start: Tuple[int, int]
    goal: Tuple[int, int]
    speed: float
    position: Tuple[float, float]
    path: List[Tuple[int, int]]
    constraints: Dict[str, float]
    status: str = "active"
    priority: int = 1
```

#### Methods:

##### `update_position(dt: float) -> None`
Updates agent's position based on current path and speed.

##### `calculate_path_metrics() -> Dict[str, float]`
Calculates metrics for the current path.

### TerrainType

```python
class TerrainType(Enum):
    URBAN = 1.2
    HIGHWAY = 0.8
    RESIDENTIAL = 1.5
    PARK = 1.3
    CONSTRUCTION = 2.5
    RESTRICTED = 10.0
```

### DynamicObstacle

```python
@dataclass
class DynamicObstacle:
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    radius: float
    lifetime: Optional[float] = None
```

## Visualization Components

### SimulationRenderer

```python
class SimulationRenderer:
    def __init__(self, grid_size: Tuple[int, int])
    def create_animation(self, frames: List[Dict], grid: List[List[GridCell]], 
                        output_path: Optional[str] = None) -> None
```

### SimulationAnalyzer

```python
class SimulationAnalyzer:
    def save_analysis(self, output_dir: str, agents: Dict, 
                     traffic_manager, simulation_time: float) -> str
```

## Traffic Management

### TrafficManager

```python
class TrafficManager:
    def update_congestion(self, pos: Tuple[int, int]) -> None
    def get_congestion_cost(self, pos: Tuple[int, int]) -> float
    def reserve_path(self, agent_id: str, path: List[Tuple[int, int]], 
                    time_windows: List[float]) -> None
```