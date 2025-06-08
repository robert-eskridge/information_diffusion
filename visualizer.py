import matplotlib.pyplot as plt
import networkx as nx
import random
from color_functions import *
from random_events import random_event_choice

# PROGRAM CONSTANTS
INFLUENCE_MINIMUM = 5

# helper function to kill dead nodes under a certain influence threshold
def murder_machine(graph, pos):
    to_remove = []
    for node in graph.nodes:
        if graph.nodes[node]["influence"]<INFLUENCE_MINIMUM:
            neighbors = list(graph[node])
            if neighbors:
                for i in range(len(neighbors)):
                    for j in range (i+1, len(neighbors)):
                        u, v = neighbors[i], neighbors[j]
                        if not graph.has_edge(u, v):
                            average_weight = (graph.get_edge_data(node, neighbors[i])["weight"] + graph.get_edge_data(node, neighbors[j])["weight"])/2
                            graph.add_edge(u, v, weight=round(average_weight, 3))
                            
                dead_influence = graph.nodes[node]["influence"]
                weights = [random.random() for _ in neighbors]  # Random weights
                total = sum(weights)
                proportions = [w / total for w in weights]      # Normalize

                for neighbor, share in zip(neighbors, proportions):
                    gain = share * dead_influence
                    graph.nodes[neighbor]["influence"] += gain
                    
            to_remove.append(node)
    graph.remove_nodes_from(to_remove)
    pos = nx.spring_layout(graph, pos=pos, fixed=graph.nodes)
    return pos

def steal_influence(graph, node):
    neighbors = graph[node]

# function specifically for MCS nodes to make their influence bigger for the MCS event duration
def MCS_influence_change(graph):
    for _, data in graph.nodes(data = True):
        if data.get("MCS") == True:
            print(f"Node with MCS: {_}")
            data["influence"] *= random.uniform(1.15, 1.5)

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
        updated_influence = current_influence * drift  
        new_influence[node] = updated_influence
    
    # update the color and influence of the nodes
    for node, new_color in new_colors.items():
        graph.nodes[node]['hex_code'] = new_color
        graph.nodes[node]['influence'] = new_influence[node]
    
    all_weights = [data["weight"] for _, _, data in graph.edges(data=True)]
    average_weight = sum(all_weights) / len(graph.edges)
    
    # update the weights randomly
    for _, _, data in graph.edges(data=True):
        if data.get("invader")==True and data["weight"] > average_weight+0.1:
            data["weight"] *= random.uniform(0.6, 0.8)
        drift = 1 + random.uniform(-weight_change_range, weight_change_range)
        data["weight"] = round(max(0.01, data["weight"] * drift), 3)
    

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
        #print(f"Influence on step {i+1}: {node_influence_dict}")
        
        node_color = [node_color_dict[node] for node in graph.nodes()]
        node_size = [node_influence_dict[node]*15 for node in graph.nodes()]
        
        edge_labels = nx.get_edge_attributes(graph, "weight")
        edge_colors = [weight_to_gray(edge_labels.get(edge, 0)) for edge in graph.edges()]
        
        nx.draw(graph, pos, with_labels=True, node_color=node_color, node_size=node_size, edge_color=edge_colors)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        
        iterate_helper(graph, influence_change_range, weight_change_range)
        MCS_influence_change(graph)
        pos = murder_machine(graph, pos)
        
        if i % event_skip==1: 
            # running random event is intentionally after iterate_helper to give a chance to visualize changes
            print(f"Random event time! On step {i+1}")
            nx.set_node_attributes(graph, False, "MCS") # reset MCS
            graph, pos = random_event_choice(graph, pos, random.choice([1,3]))
            #graph, pos = random_event_choice(graph, pos, 3)
        plt.pause(1.5)
    plt.show()