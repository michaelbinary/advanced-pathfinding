import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from ..core.grid import TerrainType
from rich.progress import Progress


class SimulationRenderer:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.fig, self.ax = plt.subplots(figsize=(12, 12))

    def render_frame(self, frame, grid):
        self.ax.clear()
        artists = []

        # Draw terrain
        terrain_colors = np.zeros((self.grid_size[0], self.grid_size[1], 3))
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                cell = grid[x][y]
                color_name = TerrainType.get_color(cell.terrain)
                color_rgb = plt.cm.colors.to_rgb(color_name)
                terrain_colors[x, y] = color_rgb

        im = self.ax.imshow(terrain_colors)
        artists.append(im)

        # Draw dynamic obstacles
        for obstacle in frame['obstacles']:
            circle = patches.Circle(
                obstacle.position,
                obstacle.radius,
                color='red',
                alpha=0.5
            )
            self.ax.add_patch(circle)
            artists.append(circle)

        # Draw agents
        for agent in frame['agents'].values():
            if agent.status != "finished":
                # Draw current position
                point = self.ax.plot(agent.position[1], agent.position[0], 'bo')[0]
                artists.append(point)

                # Draw path
                if agent.path:
                    path_x, path_y = zip(*[(p[1], p[0]) for p in agent.path])
                    path_line = self.ax.plot(path_x, path_y, 'b--', alpha=0.5)[0]
                    artists.append(path_line)

                # Draw goal
                goal_point = self.ax.plot(agent.goal[1], agent.goal[0], 'g*')[0]
                artists.append(goal_point)

        # Draw congestion
        for pos, level in frame['congestion'].items():
            if level > 1:
                rect = patches.Rectangle(
                    (pos[1] - 0.5, pos[0] - 0.5),
                    1, 1,
                    color='yellow',
                    alpha=min(level * 0.1, 0.8)
                )
                self.ax.add_patch(rect)
                artists.append(rect)

        self.ax.grid(True)
        self.ax.set_title(f'Time: {frame["time"]:.1f}s')

        return artists

    def create_animation(self, frames, grid, output_path=None):
        """Create and save the animation with progress tracking"""

        def update(frame_number):
            return self.render_frame(frames[frame_number], grid)

        anim = FuncAnimation(
            self.fig,
            update,
            frames=len(frames),
            interval=50,
            blit=True,
            repeat=False
        )

        if output_path:
            with Progress() as progress:
                task = progress.add_task("[cyan]Saving animation...", total=100)

                # Optimize GIF settings for faster saving
                anim.save(
                    output_path,
                    writer='pillow',
                    fps=10,  # Reduced FPS
                    dpi=72,  # Lower DPI
                    progress_callback=lambda i, n: progress.update(
                        task,
                        completed=int(100 * i / n)
                    )
                )

                progress.update(task, completed=100)

        plt.show()