import random
import networkx as nx
from color_functions import *

# PROGRAM CONSTANTS
AFFECTED_NODE_PERCENTAGE = 0.125
INVADER_INFLUENCE_CAP = 150

# random events:
# 1: INVASION!: 1/8 of total nodes are added to the graph, with very high influence and random placement
# 2: Plague: All nodes influence shrinks by between 25 and 75 percent
# 3: MCS (main character syndrome): 1/8 of current nodes have their influence increased every iteration until next event
# 4: City rezoning: Weights are redone with new random values
# 5: Alien Abduction: 1/8 of total nodes are removed from graph

def random_event_choice(graph, pos, event):
    if event==1:
        graph, pos = invasion_capped(graph, pos)
    if event==2:
        plague(graph)
    if event==3:
        main_character_syndrome(graph)
    if event==4:
        city_rezoning(graph)
    return graph, pos

def invasion_capped(graph, pos):
    print("Invasion!")
    nodes = list(graph.nodes)
    num_invader_nodes = int(AFFECTED_NODE_PERCENTAGE*len(nodes))
    rgb = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    hex_invaders = encode_to_hex(rgb)

    all_influence = nx.get_node_attributes(graph, "influence")
    average_influence = int(sum(all_influence))
    
    list_invader_nodes = []
    invaded = []

    for i in range(num_invader_nodes):
        invader_id = max(graph.nodes, default=-1)+1
        list_invader_nodes.append(invader_id)
        graph.add_node(invader_id)
        graph.nodes[invader_id]["hex_code"] = hex_invaders
        graph.nodes[invader_id]["influence"] = average_influence*2
        graph.nodes[invader_id]["invader"] = True

        remaining_budget = average_influence*1.5

        # Sort potential targets by cost (influence), ascending
        potential_targets = sorted(
            [n for n in graph.nodes if n != invader_id and not graph.has_edge(invader_id, n)],
            key=lambda n: graph.nodes[n]["influence"]
        )

        if random.uniform(-.25,1) < 0:
            print("Idiot invaders!")
            potential_targets.reverse()
            #print(f"First three targets: {potential_targets[:3]}")

        for target in potential_targets:
            target_cost = graph.nodes[target]["influence"]
            if target_cost <= remaining_budget and target not in invaded:
                graph.add_edge(invader_id, target, weight=0.95, invader=True)
                invaded.append(target)
                #print(f"Invaded {target} with influence cost {target_cost}!")
                remaining_budget -= target_cost
            if remaining_budget <= 0:
                break
    for i in range(len(list_invader_nodes)):
                    for j in range (i+1, len(list_invader_nodes)):
                        u, v = list_invader_nodes[i], list_invader_nodes[j]
                        if not graph.has_edge(u, v):
                            graph.add_edge(u, v, weight=.999)
    new_pos = nx.spring_layout(graph, pos=pos, fixed=pos.keys())
    return graph, new_pos

def plague(graph):
    print("Plague!")
    for node in graph.nodes:
        current_influence = graph.nodes[node]["influence"]
        drift = 1 + random.uniform(-.75, -.25)  # e.g. ±5%
        updated_influence = current_influence * drift
        graph.nodes[node]["influence"] = updated_influence

def main_character_syndrome(graph):
    nodes = list(graph.nodes)
    num_MCS_nodes = int(AFFECTED_NODE_PERCENTAGE * len(nodes))
    MCS_nodes = random.sample(nodes, min(num_MCS_nodes, len(nodes)))

    mcs_attributes = {node: True for node in MCS_nodes}
    nx.set_node_attributes(graph, mcs_attributes, "MCS")

    print(f"MCS applied to nodes: {MCS_nodes}")
    
def city_rezoning(graph):
    print("City rezoning!")

    all_edges = list(graph.edges)
    current_weights = [graph[u][v]["weight"] for u, v in all_edges]
    random.shuffle(current_weights)

    # Reassign shuffled weights to the edges
    for (u, v), new_weight in zip(all_edges, current_weights):
        graph[u][v]["weight"] = new_weight