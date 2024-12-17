import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create the airspace graph
def create_airspace_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (1, 2, 5), (1, 3, 8), (2, 4, 3),
        (3, 4, 2), (4, 5, 1), (2, 5, 10),
        (3, 5, 6), (1, 4, 9)
    ])
    return G

# Step 2: Update traffic density dynamically
def update_traffic_density(graph, d_max):
    updated_nodes = []
    for u, v, data in graph.edges(data=True):
        traffic_density = np.random.uniform(0.5, 1.5)  # Simulating real-time traffic density
        if traffic_density > d_max:
            graph[u][v]['weight'] += traffic_density
            updated_nodes.append((u, v))
    return graph, updated_nodes

# Step 3: Visualize the graph
def visualize_graph(graph, updated_nodes=None, title="Airspace Graph"):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=700)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    if updated_nodes:
        edges = [(u, v) for u, v in updated_nodes]
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2, label='Updated Edges')
    plt.title(title)
    plt.legend(["Updated edges"], loc="best")
    plt.show()

# Step 4: Demonstrate the algorithm
def demonstrate_algorithm():
    airspace = create_airspace_graph()
    d_max = 1.0  # Threshold for maximum allowed traffic density

    print("Initial Airspace Graph:")
    visualize_graph(airspace, title="Initial Airspace Graph")

    # Update graph dynamically based on traffic density
    airspace, updated_nodes = update_traffic_density(airspace, d_max)
    print("\nUpdated Airspace Graph with High-Density Zones Highlighted:")
    visualize_graph(airspace, updated_nodes, title="Updated Airspace Graph")

demonstrate_algorithm()

