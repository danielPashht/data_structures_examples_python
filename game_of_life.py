import numpy as np

from scipy.signal import convolve2d

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the grid size
GRID_SIZE = 30

# Define the convolution kernel for counting neighbors
# This kernel sums up all 8 neighbors of a cell
KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

# --- Game of Life Rules ---
# B3/S23 (Conway's original)
# A cell is Born if it has 3 neighbors.
# A cell Survives if it has 2 or 3 neighbors.
BORN_RULE = [3]
SURVIVE_RULE = [2, 3]

# B36/S23 ("HighLife" variation)
BORN_RULE = [3, 6]
SURVIVE_RULE = [2, 3]
# --------------------------

# Initialize random grid with 0s (dead) and 1s (alive)
# np.random.choice creates a random array with values 0 or 1
grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.8, 0.2])

def update(frameNum, img, grid):
    """
    Update function called for each animation frame.
    Implements Conway's Game of Life rules using convolution for performance.
    """
    # Use convolution to count live neighbors for each cell.
    # 'wrap' mode handles the toroidal grid edges perfectly.
    neighbor_count = convolve2d(grid, KERNEL, mode='same', boundary='wrap')

    # Apply the rules of life using boolean logic for efficiency
    # 1. A cell is born if it's dead (grid==0) and has a neighbor count in BORN_RULE.
    born = (grid == 0) & (np.isin(neighbor_count, BORN_RULE))
    
    # 2. A cell survives if it's alive (grid==1) and has a neighbor count in SURVIVE_RULE.
    survives = (grid == 1) & (np.isin(neighbor_count, SURVIVE_RULE))

    # Create the new grid by combining cells that are born or survive
    new_grid = grid.copy()
    new_grid[born | survives] = 1
    new_grid[~(born | survives)] = 0
    
    # Update the image data and copy new_grid to grid
    img.set_data(new_grid)
    grid[:] = new_grid
    return img,

# Set up the figure and axis
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='binary')
ax.set_title("Conway's Game of Life")
ax.axis('off')

# Create animation: calls update() every 100ms
ani = animation.FuncAnimation(fig, update, fargs=(img, grid),
                              frames=200, interval=200, save_count=50)

# --- Pause/Resume functionality ---
paused = False
def toggle_pause(event):
    global paused
    if event.key == ' ':
        paused = not paused
        if paused:
            ani.event_source.stop()
            ax.set_title("Conway's Game of Life (Paused)")
        else:
            ani.event_source.start()
            ax.set_title("Conway's Game of Life")
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('key_press_event', toggle_pause)
# ------------------------------------
plt.show()