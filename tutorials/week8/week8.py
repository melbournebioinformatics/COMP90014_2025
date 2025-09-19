import math
import time
import random
import networkx as nx 
from copy import deepcopy
from typing import Tuple
import Levenshtein

##################
### EXERCISE 1 ###
##################

def sequence_similarity(soln: list, R: nx.Graph, Q: nx.Graph) -> float:
    """
    Calculates sequence similarity using edit distance
    Returned value is a measure of dissimilarity (distance) between 0 and 1.
    Eg a perfect solution returns a value of 0. 
    """
    obs_edits, pos_edits = 0, 0
    for r_node, q_node in soln:
        if r_node is None or q_node is None:
            continue
        else:
            seq1, seq2 = R.nodes[r_node]['sequence'], Q.nodes[q_node]['sequence']
            obs_edits += Levenshtein.distance(seq1, seq2)
            pos_edits += max([len(seq1), len(seq2)])
    sequence_distance = obs_edits / pos_edits
    return sequence_distance
##################
### EXERCISE 2 ###
##################
def topological_similarity(soln: list, R: nx.Graph, Q: nx.Graph) -> float:
    """
    Calculates topological similarity
    Returned value is a measure of dissimilarity (distance) between 0 and 1.
    Eg a perfect solution returns a value of 0. 
    """
    # topological similarity (using Edge Correctness, EC)
    graph2_mapper = {r_node: q_node for r_node, q_node in soln if r_node is not None}
    total_edges = len(list(R.edges()))
    mapped_edges = 0
    for r_node1, r_node2 in R.edges():
        q_node1, q_node2 = graph2_mapper[r_node1], graph2_mapper[r_node2]
        if Q.has_edge(q_node1, q_node2):
            mapped_edges += 1
    topological_distance = 1 - (mapped_edges / total_edges)
    return topological_distance

##################
### EXERCISE 3 ###
##################

def generate_neighbour(c_solution: list) -> list:
    # randomly pick which node mappings to swap
    swap1, swap2 = random.sample(range(0, len(c_solution)), 2)
    n_solution = deepcopy(c_solution)
    n_solution[swap1][1], n_solution[swap2][1] = n_solution[swap2][1], n_solution[swap1][1]
    return n_solution


##################
### EXERCISE 4 ###
##################

def acceptance(c_energy: float, n_energy: float, temp: float) -> float:
    if n_energy < c_energy:
        return 1
    return math.exp(-(n_energy - c_energy) / temp)


##################
### EXERCISE 5 ###
##################


def simulated_annealing(R: nx.Graph, Q: nx.Graph, k_max: int=10000) -> Tuple:
    # initialise random starting state and fitness score
    c_energy = 1
    c_solution = [
        ['J', 'K'], ['I', 'A`'], ['H', 'I`'], ['G', 'H`'], ['F', 'G`'],
        ['E', 'F`'], ['D', 'E`'], ['C', 'D`'], ['B', 'C`'], ['A', 'B`'], [None, 'J`'],
    ]

    # iterate
    for k in range(k_max):
        time.sleep(0.0005)
        temp = 1 - (k/k_max)
        print(f'temp={temp:0.2f}, energy={c_energy:0.2f}', end='\r')

        # generate & assess neighbour solution
        n_solution = generate_neighbour(c_solution)
        n_energy = objective_function(n_solution, R, Q)
        acc_p = acceptance(c_energy, n_energy, temp)
        random_number = random.random()
        # Accept new solution
        if random_number < acc_p:
            c_solution = n_solution
            c_energy = n_energy

    return c_energy, c_solution


