import time
from queue import PriorityQueue

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# Define the airspace as a graph
def create_airspace_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (1, 2, 5), (1, 3, 10), (2, 4, 3),
        (3, 4, 1), (4, 5, 2), (2, 5, 8),
        (3, 5, 4), (1, 4, 7)
    ])
    return G


# Find the optimal route considering multiple factors (energy, risk, distance)
def find_optimal_route_with_factors(graph, start, end):
    def cost_function(weight, energy_factor=0.6, risk_factor=0.4):
        return energy_factor * weight + risk_factor * (1 / (1 + weight))

    pq = PriorityQueue()
    pq.put((0, start, [start]))
    visited = set()

    while not pq.empty():
        (cost, current_node, path) = pq.get()

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end:
            return path, cost

        for neighbor, edge_data in graph[current_node].items():
            weight = edge_data['weight']
            total_cost = cost + cost_function(weight)
            pq.put((total_cost, neighbor, path + [neighbor]))

    return None, float('inf')


# Kalman Filter for predicting UAV positions
def kalman_filter_example(data, noise=0.5):
    n = len(data)
    predictions = np.zeros(n)
    predictions[0] = data[0]
    for t in range(1, n):
        predictions[t] = predictions[t - 1] + noise * (data[t] - predictions[t - 1])
    return predictions


# Simulate streaming data and update the system
def simulate_streaming_data(graph, start, end, num_steps=10):
    positions = [start]
    current_node = start

    print("Simulating real-time data processing...")
    for _ in range(num_steps):
        # Simulate real-time movement
        neighbors = list(graph[current_node])
        if not neighbors:
            break
        next_node = np.random.choice(neighbors)
        positions.append(next_node)
        current_node = next_node

        # Simulate dynamic update of the airspace
        if np.random.rand() > 0.7:  # Randomly update weights or add edges
            edge_to_update = (1, 3)
            if edge_to_update in graph.edges:
                graph[edge_to_update[0]][edge_to_update[1]]['weight'] += np.random.randint(-2, 3)

        # Predict positions using Kalman filter
        predictions = kalman_filter_example(positions)
        print(f"Real-time positions: {positions}")
        print(f"Kalman Filter Predictions: {predictions}")

        # Visualize the graph and the path
        visualize_graph(graph, path=positions)

        # Pause to simulate real-time streaming
        time.sleep(1)


# Visualize the airspace graph
def visualize_graph(graph, path=None):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    plt.title("Airspace Graph with Real-Time Path")
    plt.show()


# Main function to run the simulation
def main():
    airspace = create_airspace_graph()
    start, end = 1, 5
    simulate_streaming_data(airspace, start, end, num_steps=10)


main()
