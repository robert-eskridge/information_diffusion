import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# PROGRAM CONSTANTS
NUM_NODES = 20 # how many nodes to create in the graph
EDGE_PROBABILITY = 0.15 # probability of an edge between nodes in random graph

NUM_ITERATIONS = 20 # number of iterations of color mixing to undergo

# helper function encoding a tuple in format (r,g,b) to hex value
def encode_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

# helper function decoding hex in format #ffffff to rgb tuple
def decode_from_hex(hex):
    return tuple(int(hex[i:i+2], 16) for i in (1,3,5))

# helper function that mixes colors based on weights. colors is a list of color tuples. 
# weights is a list of weights adding to 1. Use this to mix colors of neighboring nodes, normalizing their influence
# against each other to get a value of 1.
def mix_colors(colors, weights):
    r = sum(c[0] * w for c, w in zip(colors, weights))
    g = sum(c[1] * w for c, w in zip(colors, weights))
    b = sum(c[2] * w for c, w in zip(colors, weights))
    return encode_to_hex((int(r), int(g), int(b)))

# function that assigns random hex code RGB values to every node in the graph
def assign_hex_values(graph):
    values = {}
    for node in graph.nodes:
        rgb = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        values[node] = encode_to_hex(rgb)
    nx.set_node_attributes(graph, values, "hex_code")
    print(f"Values for hex color: {values}")

# function that assigns random "influence" values to each node in the form of weights
def assign_influence(graph):
    values = {}
    for node in graph.nodes:
        influence =random.randint(0,100)
        values[node] = influence
    nx.set_node_attributes(graph, values, "influence")
    print(f"Values for influence: {values}")



# function that creates a random weighted graph
def create_weighted_connected_random():
    G = nx.erdos_renyi_graph(NUM_NODES, EDGE_PROBABILITY)
    #   ensure that the graph is always connected by killing graphs
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(NUM_NODES, EDGE_PROBABILITY)
        print("Iterated through another graph")
    nx.set_edge_attributes(G, {e: {'weight': random.randint(1, 10)} for e in G.edges})
    pos = nx.spring_layout(G) # this keeps the graph stationary while iterating in animation
    return G, pos

def visualize_graph(graph, pos):
    print("Visualizing graph!")
    for i in range(NUM_ITERATIONS):
        plt.title(f"Step {i} in graph iteration.")
        node_color_dict = nx.get_node_attributes(graph, "hex_code")
        node_color = [node_color_dict[node] for node in graph.nodes()]
        nx.draw(graph, pos, with_labels=True, node_color=node_color)
        plt.show()
        time.sleep(2)


G, pos = create_weighted_connected_random()
print(f"Nodes in graph: {G.nodes}")
assign_influence(G)
assign_hex_values(G)
visualize_graph(G, pos)