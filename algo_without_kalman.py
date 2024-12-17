import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# Step 1: Create a graph for the airspace
def create_airspace_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (1, 2, 5), (1, 3, 8), (2, 4, 3),
        (3, 4, 2), (4, 5, 1), (2, 5, 10),
        (3, 5, 6), (1, 4, 9)
    ])
    return G


# Step 2: Simulate noisy data without Kalman Filter
def simulate_noisy_positions(real_positions, noise_level=0.5):
    noisy_positions = real_positions + np.random.normal(0, noise_level, len(real_positions))
    return noisy_positions


# Step 3: Optimize route without dynamic updates
def optimize_route_no_update(graph, start, end):
    path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    cost = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    return path, cost


# Step 4: Visualize the graph
def visualize_graph(graph, path=None, title="Airspace Graph"):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=700)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    plt.title(title)
    plt.show()


# Step 5: Simulate traffic without Kalman filter and dynamic updates
def simulate_no_algorithm():
    airspace = create_airspace_graph()
    start, end = 1, 5
    real_positions = np.array([1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

    # Simulate noisy data
    noisy_positions = simulate_noisy_positions(real_positions)
    print(f"Real Positions: {real_positions}")
    print(f"Noisy Positions: {noisy_positions}")

    # Optimize route without updates
    print("Initial Airspace:")
    visualize_graph(airspace, title="Initial Airspace")

    path, cost = optimize_route_no_update(airspace, start, end)
    print(f"Optimal Path Without Updates: {path}, Cost: {cost}")
    visualize_graph(airspace, path, title="Optimal Path Without Updates")


simulate_no_algorithm()

