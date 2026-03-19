import heapq
import random
import time
import matplotlib.pyplot as plt
import numpy as np

class UGVStaticPlanner:
    def __init__(self, grid_size=70, density_level=1):
        """
        Initialize the UGV Planner.
        :param grid_size: Size of the map (e.g., 70x70)
        :param density_level: 1 (Low), 2 (Medium), 3 (High)
        """
        self.grid_size = grid_size
        self.density_level = density_level
        self.grid = np.zeros((grid_size, grid_size), dtype=int) # 0: Free, 1: Obstacle
        self.start = (5, 5)
        self.goal = (grid_size - 6, grid_size - 6)
        
    def generate_map(self):
        """Generates random static obstacles based on density level."""
        densities = {1: 0.10, 2: 0.25, 3: 0.40}
        prob = densities.get(self.density_level, 0.25)
        
        print(f"Generating map with Density Level {self.density_level} ({prob*100}% occupancy)...")
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                # Don't place obstacles on start or goal initially
                if (r, c) == self.start or (r, c) == self.goal:
                    continue
                
                if random.random() < prob:
                    self.grid[r, c] = 1
        
        # Double check start/goal are clear (in case logic above failed due to randomness edge cases)
        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def get_neighbors(self, node):
        """Returns valid neighbors (Up, Down, Left, Right) with cost 1."""
        r, c = node
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check boundaries
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                # Check if not an obstacle
                if self.grid[nr, nc] == 0:
                    neighbors.append(((nr, nc), 1)) # Cost is 1
        return neighbors

    def dijkstra_search(self):
        """Implements Dijkstra/Uniform-Cost Search."""
        # Priority Queue: (cost, node)
        pq = [(0, self.start)]
        came_from = {self.start: None}
        cost_so_far = {self.start: 0}
        nodes_expanded = 0
        
        start_time = time.time()
        
        while pq:
            current_cost, current = heapq.heappop(pq)
            nodes_expanded += 1
            
            if current == self.goal:
                break
            
            for next_node, move_cost in self.get_neighbors(current):
                new_cost = cost_so_far[current] + move_cost
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost 
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current
                    
        end_time = time.time()
        
        # Reconstruct path
        path = []
        curr = self.goal
        if curr not in came_from and curr != self.start:
            return None, {"path_length": 0, "computation_time": 0, "nodes_expanded": 0}, float('inf')
            
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        
        measures = {
            "path_length": len(path) - 1, # Steps taken
            "computation_time": end_time - start_time,
            "nodes_expanded": nodes_expanded
        }
        
        return path, measures, cost_so_far.get(self.goal, float('inf'))

    def visualize(self, path):
        """Visualizes the grid, obstacles, and the calculated path."""
        plt.figure(figsize=(10, 10))
        plt.imshow(self.grid, cmap='binary', origin='upper') # Black=Obstacle, White=Free
        
        if path:
            path_y, path_x = zip(*path)
            plt.plot(path_x, path_y, color='red', linewidth=2.5, label='Optimal Path')
            plt.plot(self.start[1], self.start[0], 'go', markersize=15, label='Start Node')
            plt.plot(self.goal[1], self.goal[0], 'bo', markersize=15, label='Goal Node')
        
        plt.title(f"UGV Static Navigation (Density: {self.density_level})")
        plt.legend(loc='upper right')
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.show()

def main():
    print("--- PART 2: UGV Static Obstacle Navigation ---")
    
    # Configuration
    GRID_SIZE = 70
    DENSITY_LEVEL = 2 # Try 1, 2, or 3
    
    planner = UGVStaticPlanner(grid_size=GRID_SIZE, density_level=DENSITY_LEVEL)
    planner.generate_map()
    
    print("Running Dijkstra's Algorithm...")
    path, measures, total_dist = planner.dijkstra_search()
    
    if path:
        print("\n*** Results ***")
        print(f"Status: Path Found Successfully")
        print(f"Measures of Effectiveness:")
        print(f"  1. Total Distance (Steps): {measures['path_length']}")
        print(f"  2. Computation Time:       {measures['computation_time']:.5f} seconds")
        print(f"  3. Nodes Expanded:         {measures['nodes_expanded']}")
        
        planner.visualize(path)
    else:
        print("\n*** Results ***")
        print("Status: NO PATH FOUND (Obstacles block all routes)")
        print("Try lowering the density level and running again.")

if __name__ == "__main__":
    main()