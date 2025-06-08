import matplotlib.pyplot as plt
import networkx as nx
import random
from color_functions import *
from random_events import random_event_choice

# helper function that mixes colors in graph
def iterate_helper(graph, influence_change_range, weight_change_range):
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
    
    all_weights = [data["weight"] for _, _, data in graph.edges(data=True)]
    average_weight = sum(all_weights) / len(graph.edges)
    
    for _, _, data in graph.edges(data=True):
        if data.get("invader")==True and data["weight"] > average_weight+0.1:
            data["weight"] *= random.uniform(0.6, 0.8)
        drift = 1 + random.uniform(-weight_change_range, weight_change_range)
        data["weight"] = round(max(0.01, min(data["weight"] * drift, 100)), 3)
    

def visualize_graph(graph, pos, iterations, influence_change_range, weight_change_range, event_skip):
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
        
        iterate_helper(graph, influence_change_range, weight_change_range)
        
        if i % event_skip==1: 
            # running random event is intentionally after iterate_helper to give a chance to visualize changes
            print(f"Random event time! On step {i+1}")
            graph, pos = random_event_choice(graph, pos, 1)
        plt.pause(1.5)
    plt.show()