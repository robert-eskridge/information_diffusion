import matplotlib.pyplot as plt
import networkx as nx
import random
from color_functions import *

# helper function that mixes colors in graph
def iterate_helper(graph):
    new_colors = {}
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
    
    for node, new_color in new_colors.items():
        graph.nodes[node]['hex_code'] = new_color
    

def visualize_graph(graph, pos, iterations):
    print("Visualizing graph!")
    
    fig = plt.gcf()
    fig.set_size_inches(10, 7)  # Adjust based on your screen resolution
    fig.tight_layout()
    for i in range(iterations):
        plt.clf()
        plt.title(f"Step {i+1} in graph iteration.")
        node_color_dict = nx.get_node_attributes(graph, "hex_code")
        node_influence_dict = nx.get_node_attributes(graph, "influence")
        
        node_color = [node_color_dict[node] for node in graph.nodes()]
        node_size = [node_influence_dict[node]*15 for node in graph.nodes()]
        
        edge_labels = nx.get_edge_attributes(graph, "weight")
        edge_colors = [weight_to_gray(edge_labels.get(edge, 0)) for edge in graph.edges()]
        
        nx.draw(graph, pos, with_labels=True, node_color=node_color, node_size=node_size, edge_color=edge_colors)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        
        plt.pause(1.5)
        iterate_helper(graph)
    plt.show()