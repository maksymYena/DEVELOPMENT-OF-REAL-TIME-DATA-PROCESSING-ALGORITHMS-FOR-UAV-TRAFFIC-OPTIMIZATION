import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pykalman import KalmanFilter


# Step 1: Initialize the airspace graph
def create_airspace_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (1, 2, 5), (1, 3, 8), (2, 4, 3),
        (3, 4, 2), (4, 5, 1), (2, 5, 10),
        (3, 5, 6), (1, 4, 9)
    ])
    return G


# Step 2: Kalman filter for real-time position prediction
def apply_kalman_filter(data):
    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
    measurements = np.array(data).reshape(-1, 1)
    state_means, _ = kf.filter(measurements)
    return state_means.ravel()


# Step 3: Update traffic density dynamically
def update_traffic_density(graph, d_max):
    for u, v, data in graph.edges(data=True):
        traffic_density = np.random.uniform(0.5, 1.5)  # Simulating real-time traffic
        if traffic_density > d_max:
            graph[u][v]['weight'] += traffic_density
    return graph


# Step 4: Optimize the route
def optimize_route(graph, start, end):
    path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    cost = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    return path, cost


# Step 5: Monte Carlo simulation for delays
def monte_carlo_delays(num_samples, lam):
    delays = np.random.exponential(1 / lam, num_samples)
    return delays


# Step 6: Visualize the graph
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


# Step 7: Simulate real-time traffic optimization
def simulate_real_time():
    airspace = create_airspace_graph()
    start, end = 1, 5
    d_max = 7

    # Initial visualization
    print("Initial Airspace:")
    visualize_graph(airspace, title="Initial Airspace")

    # Apply Kalman Filter for position smoothing
    positions = [1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    smoothed_positions = apply_kalman_filter(positions)
    print(f"Original Positions: {positions}")
    print(f"Smoothed Positions (Kalman Filter): {smoothed_positions}")

    # Update graph dynamically and optimize
    airspace = update_traffic_density(airspace, d_max)
    print("\nUpdated Airspace:")
    visualize_graph(airspace, title="Updated Airspace")

    path, cost = optimize_route(airspace, start, end)
    print(f"Optimal Path: {path}, Cost: {cost}")
    visualize_graph(airspace, path, title="Optimal Path in Updated Airspace")

    # Monte Carlo simulation for delays
    delays = monte_carlo_delays(100, lam=0.5)
    avg_delay = np.mean(delays)
    print(f"Simulated Delays (Monte Carlo): {delays[:10]}")
    print(f"Average Delay: {avg_delay:.2f} seconds")


simulate_real_time()
