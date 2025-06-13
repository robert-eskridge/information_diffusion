import matplotlib.pyplot as plt
import networkx as nx
import random
from visual_helpers import *
from random_events import random_event_choice
from pyvis.network import Network

from pyvis.network import Network

def visualize_large_graph(graph):
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")

    # Optional: For physics animation on layout
    net.barnes_hut()

    for node, data in graph.nodes(data=True):
        influence = data.get("influence", 1)
        color = data.get("hex_code", "#888888")
        stubborn = data.get("stubborn", 0)

        net.add_node(
            node,
            label=str(node),
            title=f"Influence: {influence}<br>Stubbornness: {stubborn}",
            color=color,
            size=max(influence, 5)  # Prevent invisible nodes
        )

    for u, v, data in graph.edges(data=True):
        weight = data.get("weight", 1)
        net.add_edge(
            u,
            v,
            value=weight,
            title=f"Weight: {weight:.2f}"
        )

    net.show("diffusion.html", notebook=False)
    
#TODO refactor this into pyvis network instead of matplotlib
def visualize_graph(graph, pos, iterations, influence_change_range, weight_change_range, event_skip):
    print("Visualizing graph!")
    
    fig = plt.gcf()
    fig.set_size_inches(10, 7)  # Adjust based on your screen resolution
    fig.tight_layout()
    
    last_event = 9999
    
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
        
        simulate_drift(graph, influence_change_range, weight_change_range)
        MCS_influence_change(graph)
        steal_influence(graph)
        pos = murder_machine(graph, pos)
        
        if i % event_skip==1: 
            # running random event is intentionally after iterate_helper to give a chance to visualize changes
            print(f"Random event time! On step {i+1}")
            nx.set_node_attributes(graph, False, "MCS") # reset MCS
            new_event = random.choice([1,6])
            while new_event==last_event:
                new_event = random.choice([1,6])
            graph, pos = random_event_choice(graph, pos, new_event)
            #graph, pos = random_event_choice(graph, pos, 6)
            last_event = new_event
        plt.pause(1.5)
    plt.show()