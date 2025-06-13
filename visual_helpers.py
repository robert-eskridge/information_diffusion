import networkx as nx
import random
from color_functions import *

# PROGRAM CONSTANTS
INFLUENCE_MINIMUM = 5

# helper function to kill dead nodes under a certain influence threshold
def murder_machine(graph, pos):
    to_remove = []
    for node in list(graph.nodes):
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


def steal_influence(graph):
    new_influence = {}

    for node in graph.nodes:
        current_influence = graph.nodes[node]["influence"]
        influence_gain = 0
        influence_loss = {}

        for neighbor in graph[node]:
            neighbor_influence = graph.nodes[neighbor]["influence"]
            weight = graph.get_edge_data(node, neighbor)["weight"]
            if neighbor_influence > 2 * current_influence:
                influence_gain += current_influence * 0.1 * weight  # Node gains 10%
                influence_loss[neighbor] = influence_loss.get(neighbor, 0) + neighbor_influence * 0.09 * weight  # Neighbor loses 9%

        new_influence[node] = current_influence + influence_gain

        for n, loss in influence_loss.items():
            new_influence[n] = graph.nodes[n]["influence"] - loss

    # Apply updates after all calculations
    for node, influence in new_influence.items():
        graph.nodes[node]["influence"] = round(max(influence, 0), 3)  # Ensure influence is not negative

# function specifically for MCS nodes to make their influence bigger for the MCS event duration
def MCS_influence_change(graph):
    for _, data in graph.nodes(data = True):
        if data.get("MCS") == True:
            data["influence"] *= random.uniform(1.15, 1.25)
            
# helper function that mixes colors in graph
def simulate_drift(graph, influence_change_range, weight_change_range):
    new_colors = {}
    new_influence = {}
    for node in graph.nodes:
        neighbors = graph[node]
        if not neighbors:
            continue
        # Grab all the influences and colors of the neighbors and of self
        all_influences = [graph.nodes[n]["influence"] * graph[node][n]["weight"]
                          * (1 - graph.nodes[n]["stubborn"] / 100) for n in neighbors]
        all_influences.append(graph.nodes[node]["influence"] * (1 - graph.nodes[node]["stubborn"] / 100))
        all_colors = [decode_from_hex(graph.nodes[n]["hex_code"]) for n in neighbors]
        all_colors.append(decode_from_hex(graph.nodes[node]["hex_code"]))
        
        # sum and normalize influence
        total_weights = sum(all_influences)
        normalized_weights = [inf / total_weights for inf in all_influences]
        
        # mix the colors of the neighbors and their normalized weights
        new_colors[node] = mix_colors(all_colors, normalized_weights)
        
        # Apply small influence change (multiplicative drift)
        THRESHOLD= 100
        current_influence = graph.nodes[node]["influence"]
        growth_factor = 1 + random.uniform(-influence_change_range, influence_change_range)
        # Diminishing growth: scale drift down based on current influence
        damping = 1 / (1 + (current_influence / THRESHOLD))  # between 0 and 1
        adjusted_drift = 1 + (growth_factor - 1) * damping
        updated_influence = current_influence*adjusted_drift
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