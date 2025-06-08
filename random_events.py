import random
import networkx as nx
from color_functions import *

AFFECTED_NODE_PERCENTAGE = 0.125

# random events:
# 1: INVASION!: 1/8 of total nodes are added to the graph, with very high influence and random placement
# 2: Plague: All nodes influence shrinks by between 25 and 75 percent
# 3: MCS (main character syndrome): 1/8 of current nodes have their influence increased every iteration until next event
# 4: City rezoning: Weights are redone with new random values
# 5: Alien Abduction: 1/8 of total nodes are removed from graph

def random_event_choice(graph, pos, event):
    if event==1:
        graph, pos = invasion(graph, pos)
    return graph, pos

def invasion(graph, pos):
    nodes = list(graph.nodes)
    num_random_nodes = int(AFFECTED_NODE_PERCENTAGE*len(nodes))
    rgb = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    hex_invaders = encode_to_hex(rgb)
    
    for i in range(num_random_nodes):
        random_node = len(nodes)+i+1
        graph.add_node(random_node)
        graph.nodes[random_node]["hex_code"] = hex_invaders
        graph.nodes[random_node]["influence"] = 99
        invaded_one, invaded_two = random.choice(list(graph.edges))
        graph.add_edge(random_node, invaded_one, weight=0.95, invader = True)
        graph.add_edge(random_node, invaded_two, weight=0.95, invader = True)
    new_pos = nx.spring_layout(graph, pos=pos, fixed=pos.keys())
    return graph, new_pos