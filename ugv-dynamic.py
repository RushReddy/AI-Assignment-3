import random
import math
import matplotlib.pyplot as plt
import numpy as np

class UGVDynamicPlanner:
    def __init__(self, grid_size=50, static_density=0.15):
        self.grid_size = grid_size
        self.static_density = static_density
        self.grid = np.zeros((grid_size, grid_size), dtype=int) # Static obstacles
        self.dynamic_obstacles = [] # List of [row, col, vel_r, vel_c]
        
        self.start = (5, 5)
        self.goal = (grid_size - 6, grid_size - 6)
        
    def generate_static_map(self):
        """Generate fixed obstacles."""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) == self.start or (r, c) == self.goal:
                    continue
                if random.random() < self.static_density:
                    self.grid[r, c] = 1
                    
    def add_dynamic_obstacles(self, count=8):
        """Add moving obstacles with random velocities."""
        for _ in range(count):
            while True:
                r = random.randint(10, self.grid_size-10)
                c = random.randint(10, self.grid_size-10)
                # Ensure not on top of static obstacles or start/goal
                if self.grid[r, c] == 0 and (r,c) != self.start and (r,c) != self.goal:
                    # Random velocity (-1, 0, or 1)
                    vr = random.choice([-1, 0, 1])
                    vc = random.choice([-1, 0, 1])
                    # Ensure it actually moves
                    if vr == 0 and vc == 0:
                        vr = 1
                    self.dynamic_obstacles.append([float(r), float(c), vr, vc])
                    break

    def update_dynamic_positions(self):
        """Move dynamic obstacles and handle wall bouncing."""
        # We return a temporary grid that combines static + current dynamic positions
        temp_grid = self.grid.copy()
        
        for obs in self.dynamic_obstacles:
            # Update position
            obs[0] += obs[2]
            obs[1] += obs[3]
            
            # Bounce off walls
            if not (0 <= obs[0] < self.grid_size):
                obs[2] *= -1
                obs[0] += obs[2] # Step back in
            if not (0 <= obs[1] < self.grid_size):
                obs[3] *= -1
                obs[1] += obs[3]
            
            # Mark occupied in temp grid
            r_int, c_int = int(round(obs[0])), int(round(obs[1]))
            temp_grid[r_int, c_int] = 1
            
        return temp_grid

    def get_safe_move(self, current_pos, temp_grid):
        """
        Decides the next best move avoiding immediate dynamic collisions.
        In a full implementation, this would call a local A*/Dijkstra replanner.
        Here we use a heuristic greedy approach with collision avoidance.
        """
        r, c = current_pos
        gr, gc = self.goal
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        best_move = None
        min_heuristic = float('inf')
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                # Check collision with ANY obstacle (static or dynamic in temp_grid)
                if temp_grid[nr, nc] == 0:
                    # Calculate Euclidean distance to goal
                    dist = math.sqrt((nr - gr)**2 + (nc - gc)**2)
                    
                    # Add a small penalty for getting too close to dynamic obstacles centers?
                    # For simplicity, we just ensure temp_grid is 0.
                    
                    if dist < min_heuristic:
                        min_heuristic = dist
                        best_move = (nr, nc)
        
        return best_move

    def simulate_navigation(self, max_steps=300):
        """Runs the simulation loop."""
        current_pos = self.start
        path_history = [current_pos]
        collision = False
        
        print(f"Starting Dynamic Simulation...")
        print(f"Start: {self.start}, Goal: {self.goal}")
        
        for step in range(max_steps):
            if current_pos == self.goal:
                print(f"\nSuccess! Reached goal in {step} steps.")
                return path_history, False
            
            # 1. Update World (Move obstacles)
            temp_grid = self.update_dynamic_positions()
            
            # 2. Check if current position is suddenly occupied (Collision)
            if temp_grid[current_pos] == 1:
                print(f"\nCollision detected at step {step}! Mission Failed.")
                collision = True
                break
            
            # 3. Plan Next Move
            next_pos = self.get_safe_move(current_pos, temp_grid)
            
            if next_pos:
                current_pos = next_pos
                path_history.append(current_pos)
                
                # Debug output every 20 steps
                if step % 20 == 0:
                    dist_to_goal = math.sqrt((current_pos[0]-self.goal[0])**2 + (current_pos[1]-self.goal[1])**2)
                    print(f"Step {step}: At {current_pos}, Dist to Goal: {dist_to_goal:.2f}")
            else:
                # No safe moves available (trapped)
                print(f"\nRobot trapped at step {step}. No safe moves available.")
                break
                
        if not collision and current_pos != self.goal:
            print(f"\nSimulation timed out after {max_steps} steps.")
            
        return path_history, collision

    def visualize_simulation(self, path_history, collision):
        plt.figure(figsize=(10, 10))
        # Plot static obstacles
        plt.imshow(self.grid, cmap='gray', origin='upper', alpha=0.3)
        
        # Plot dynamic obstacles final positions
        if self.dynamic_obstacles:
            dyn_y = [int(o[0]) for o in self.dynamic_obstacles]
            dyn_x = [int(o[1]) for o in self.dynamic_obstacles]
            plt.scatter(dyn_x, dyn_y, c='orange', s=150, marker='X', label='Dynamic Obstacles (Final)')
        
        # Plot Path
        if path_history:
            py, px = zip(*path_history)
            color = 'red' if collision else 'green'
            label = 'Collision Path' if collision else 'Successful Path'
            plt.plot(px, py, color=color, linewidth=2, label=label)
            
            plt.plot(self.start[1], self.start[0], 'go', markersize=12, label='Start')
            plt.plot(self.goal[1], self.goal[0], 'bo', markersize=12, label='Goal')
        
        plt.title(f"UGV Dynamic Navigation {'(Failed)' if collision else '(Success)'}")
        plt.legend()
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.show()

def main():
    print("--- PART 3: UGV Dynamic Obstacle Navigation ---")
    
    # Setup
    planner = UGVDynamicPlanner(grid_size=50, static_density=0.15)
    planner.generate_static_map()
    planner.add_dynamic_obstacles(count=6) # 6 moving obstacles
    
    # Run
    path, crashed = planner.simulate_navigation(max_steps=400)
    
    # Visualize
    planner.visualize_simulation(path, crashed)

if __name__ == "__main__":
    main()