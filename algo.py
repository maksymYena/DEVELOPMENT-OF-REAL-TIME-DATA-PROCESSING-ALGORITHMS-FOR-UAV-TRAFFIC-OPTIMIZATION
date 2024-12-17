import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pykalman import KalmanFilter

# Create airspace graph
def create_airspace_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (1, 2, 5), (1, 3, 8), (2, 4, 3),
        (3, 4, 2), (4, 5, 1), (2, 5, 10),
        (3, 5, 6), (1, 4, 9)
    ])
    return G

# Update traffic density in real-time
def update_traffic_density(graph, d_max):
    for u, v, data in graph.edges(data=True):
        traffic_density = np.random.uniform(0.5, 1.5)  # Simulate traffic density
        if traffic_density > d_max:
            graph[u][v]['weight'] += traffic_density
    return graph

# Kalman filter for position prediction
def kalman_filter(data):
    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
    measurements = np.array(data).reshape(-1, 1)
    state_means, _ = kf.filter(measurements)
    return state_means.ravel()

# Optimize route
def optimize_route(graph, start, end):
    path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    cost = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    return path, cost

# Visualize graph
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

# Simulate real-time traffic optimization
def simulate_real_time():
    airspace = create_airspace_graph()
    start, end = 1, 5
    d_max = 7

    # Initial visualization
    print("Initial Airspace:")
    visualize_graph(airspace, title="Initial Airspace")

    # Simulate position updates using Kalman Filter
    positions = [1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    smoothed_positions = kalman_filter(positions)
    print(f"Original Positions: {positions}")
    print(f"Smoothed Positions (Kalman Filter): {smoothed_positions}")

    # Update traffic and optimize
    airspace = update_traffic_density(airspace, d_max)
    print("\nUpdated Airspace (after density update):")
    visualize_graph(airspace, title="Airspace with Updated Densities")

    path, cost = optimize_route(airspace, start, end)
    print(f"Optimal Path: {path}, Cost: {cost}")
    visualize_graph(airspace, path, title="Optimized Path in Updated Airspace")

simulate_real_time()
