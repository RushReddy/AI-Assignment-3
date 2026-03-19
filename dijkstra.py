import networkx as nx
import matplotlib.pyplot as plt

def create_india_road_network():
    """
    Creates a weighted graph representing major Indian cities and road distances.
    Data is approximate based on common highway routes.
    """
    G = nx.Graph()
    
    # List of edges: (City A, City B, Distance in km)
    roads = [
        ("Delhi", "Jaipur", 280),
        ("Delhi", "Agra", 230),
        ("Delhi", "Lucknow", 560),
        ("Delhi", "Chandigarh", 245),
        ("Jaipur", "Ahmedabad", 660),
        ("Jaipur", "Udaipur", 390),
        ("Agra", "Gwalior", 120),
        ("Gwalior", "Bhopal", 430),
        ("Bhopal", "Nagpur", 350),
        ("Nagpur", "Hyderabad", 510),
        ("Hyderabad", "Bangalore", 570),
        ("Hyderabad", "Chennai", 630),
        ("Bangalore", "Chennai", 350),
        ("Bangalore", "Mysore", 140),
        ("Chennai", "Visakhapatnam", 890),
        ("Ahmedabad", "Mumbai", 530),
        ("Mumbai", "Pune", 150),
        ("Pune", "Bangalore", 840),
        ("Pune", "Goa", 450),
        ("Lucknow", "Varanasi", 320),
        ("Varanasi", "Patna", 250),
        ("Patna", "Kolkata", 580),
        ("Kolkata", "Bhubaneswar", 440),
        ("Bhubaneswar", "Visakhapatnam", 440),
        ("Chandigarh", "Shimla", 115),
        ("Udaipur", "Ahmedabad", 260)
    ]
    
    G.add_weighted_edges_from(roads)
    return G

def dijkstra_search(graph, start, goal):
    """
    Implements Dijkstra's Algorithm (Uniform-Cost Search) to find the shortest path.
    Returns the path list and total cost.
    """
    try:
        # NetworkX uses Dijkstra's algorithm under the hood for shortest_path with weights
        path = nx.dijkstra_path(graph, source=start, target=goal, weight='weight')
        total_cost = nx.dijkstra_path_length(graph, source=start, target=goal, weight='weight')
        return path, total_cost
    except nx.NetworkXNoPath:
        return None, float('inf')

def visualize_path(graph, path):
    """
    Visualizes the graph and highlights the optimal path in red.
    """
    if not path:
        print("No path to visualize.")
        return

    pos = nx.spring_layout(graph, seed=42, k=0.5) # k adjusts spacing
    
    plt.figure(figsize=(14, 10))
    
    # Draw all nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_color='lightblue', node_size=2500, alpha=0.9)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1, alpha=0.6)
    
    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=9, font_weight='bold')
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    
    # Highlight the optimal path
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=3)
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='orange', node_size=2500)
    
    plt.title(f"Dijkstra's Algorithm: Optimal Path from {path[0]} to {path[-1]}", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 60)
    print("Dijkstra's Algorithm (Uniform-Cost Search) Implementation")
    print("Dataset: Major Indian Cities and Road Distances")
    print("=" * 60)
    
    # 1. Create the Graph
    G = create_india_road_network()
    
    # 2. Define Start and Goal
    start_city = "Delhi"
    goal_city = "Bangalore"
    
    print(f"\nSearching for optimal path from {start_city} to {goal_city}...\n")
    
    # 3. Run Algorithm
    path, cost = dijkstra_search(G, start_city, goal_city)
    
    # 4. Output Results
    if path:
        print(f"✅ Path Found!")
        print(f"   Route: {' -> '.join(path)}")
        print(f"   Total Distance: {cost} km")
        
        # 5. Visualize
        print("\nGenerating visualization window... (Close the plot to exit)")
        visualize_path(G, path)
    else:
        print(f"❌ No path found between {start_city} and {goal_city}.")

if __name__ == "__main__":
    main()