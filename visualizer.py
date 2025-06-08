import matplotlib.pyplot as plt
import networkx as nx
import random
from color_functions import *

# helper function that mixes colors in graph
def iterate_helper(graph, influence_change_range):
    new_colors = {}
    new_influence = {}
    for node in graph.nodes:
        neighbors = graph[node]
        if not neighbors:
            continue
        # Grab all the influences and colors of the neighbors and of self
        all_influences = [graph.nodes[n]["influence"]*graph[node][n]["weight"] for n in neighbors]
        all_influences.append(graph.nodes[node]["influence"])
        all_colors = [decode_from_hex(graph.nodes[n]["hex_code"]) for n in neighbors]
        all_colors.append(decode_from_hex(graph.nodes[node]["hex_code"]))
        
        # sum and normalize influence
        total_weights = sum(all_influences)
        normalized_weights = [inf / total_weights for inf in all_influences]
        
        # mix the colors of the neighbors and their normalized weights
        new_colors[node] = mix_colors(all_colors, normalized_weights)
        # Apply small influence change (multiplicative drift)
        current_influence = graph.nodes[node]["influence"]
        drift = 1 + random.uniform(-influence_change_range, influence_change_range)  # e.g. ±5%
        updated_influence = max(1, min(current_influence * drift, 100))  # Clamp between 1 and 100
        new_influence[node] = updated_influence
    
    for node, new_color in new_colors.items():
        graph.nodes[node]['hex_code'] = new_color
        graph.nodes[node]['influence'] = new_influence[node]
    

def visualize_graph(graph, pos, iterations, influence_change_range):
    print("Visualizing graph!")
    
    fig = plt.gcf()
    fig.set_size_inches(10, 7)  # Adjust based on your screen resolution
    fig.tight_layout()
    for i in range(iterations):
        plt.clf()
        plt.title(f"Step {i+1} in graph iteration.")
        node_color_dict = nx.get_node_attributes(graph, "hex_code")
        node_influence_dict = nx.get_node_attributes(graph, "influence")
        print(f"Influence on step {i+1}: {node_influence_dict}")
        
        node_color = [node_color_dict[node] for node in graph.nodes()]
        node_size = [node_influence_dict[node]*15 for node in graph.nodes()]
        
        edge_labels = nx.get_edge_attributes(graph, "weight")
        edge_colors = [weight_to_gray(edge_labels.get(edge, 0)) for edge in graph.edges()]
        
        nx.draw(graph, pos, with_labels=True, node_color=node_color, node_size=node_size, edge_color=edge_colors)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        
        plt.pause(1.5)
        iterate_helper(graph, influence_change_range)
    plt.show()