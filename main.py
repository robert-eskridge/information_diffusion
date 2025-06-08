import networkx as nx
import matplotlib.pyplot as plt
import random
from color_functions import *
from visualizer import *

# PROGRAM CONSTANTS
NUM_NODES = 16 # how many nodes to create in the graph
SMALL_WORLD_NEIGHBORS = 4
EDGE_PROBABILITY = 0.10 # probability of an edge between nodes in random graph
NUM_ITERATIONS = 27 # number of iterations of color mixing to undergo
EVENT_SKIPS = 5 # number of iterations between events
INFLUENCE_CHANGE_RANGE = 0.5 # range of how much influence can change per iteration as a percentage
WEIGHT_CHANGE_RANGE = 0.1

# function that creates a random weighted graph
def create_weighted_connected_random():
    G = nx.erdos_renyi_graph(NUM_NODES, EDGE_PROBABILITY)
    #   ensure that the graph is always connected by killing graphs
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(NUM_NODES, EDGE_PROBABILITY)
        print("Iterated through another graph")
    nx.set_edge_attributes(G, {e: {'weight': round(random.random(), 3)} for e in G.edges})
    pos = nx.spring_layout(G) # this keeps the graph stationary while iterating in animation
    return G, pos

def create_small_world_graph():
    G = nx.watts_strogatz_graph(NUM_NODES, SMALL_WORLD_NEIGHBORS, EDGE_PROBABILITY)

    while not nx.is_connected(G):
        G = nx.watts_strogatz_graph(NUM_NODES, SMALL_WORLD_NEIGHBORS, EDGE_PROBABILITY)
        print("Iterated through another graph")
    
    nx.set_edge_attributes(G, {e: {'weight': round(random.uniform(0.1, 1.0), 3)} for e in G.edges})
    pos = nx.spring_layout(G)
    return G, pos

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

def main():
    selection = int(input("1: erdos renyi \n2: small world\n"))
    if selection==1:   
        G, pos = create_weighted_connected_random()
    elif selection==2:
        G, pos = create_small_world_graph()
    print(f"Nodes in graph: {G.nodes}")
    assign_influence(G)
    assign_hex_values(G)
    visualize_graph(G, pos, NUM_ITERATIONS, INFLUENCE_CHANGE_RANGE, WEIGHT_CHANGE_RANGE, EVENT_SKIPS)
    
# TODO add random events every XONSTANT iteration
main()