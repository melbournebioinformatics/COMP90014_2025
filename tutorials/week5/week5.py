import numpy as np
import networkx as nx

##############
# EXERCISE 1 #
##############

def init_tip(tree, tip_name, observed_nt):
    """
    Intialise a tip of a tree with the correct costs.
    At this tip node, only the observed nucleotides are possible:
    the cost of the observed nucleotide is zero, and
    the cost of any other nucleotide is infinity.
    """

    mat = tree.nodes[tip_name]['matrix']
    mat += np.inf
    mat[idx[observed_nt]] = 0
    return None


##############
# EXERCISE 2 #
##############
def sankoff_calculate(cost_matrix, tree, node_name):
    """
    For the specified node of the tree, calculate the minimum possible cost 
    for each nucleotide. 
    """
    children = list(tree.successors(node_name))
    left_mat = tree.nodes[children[0]]['matrix']
    right_mat = tree.nodes[children[1]]['matrix']

    # Repeat the child matrix to make it fit the shape of cost matrix
    # Repeat the vector across rows, from 4 by 1 to 4 by 4
    child_mat_1 = np.repeat(left_mat, 4, axis = 1)
    child_mat_1 += cost_matrix
    child_mat_2 = np.repeat(right_mat, 4, axis = 1)
    child_mat_2 += cost_matrix

    # Get the minimum across each column
    # From 4 by 4 to 1 by 4
    child_mat_1 = np.min(child_mat_1, axis = 0)
    child_mat_2 = np.min(child_mat_2, axis = 0)
    mat = child_mat_1 + child_mat_2

    # Transpose the matrix, from 1 by 4 back to 4 by 1
    tree.nodes[node_name]['matrix'] = np.reshape(mat, shape=(4, 1))
    return None

###############
# Extension 1 #
###############

### Instead of making the gap the fifth value in the cost matrix,
### you can also set every base to zero when there's a gap

# Define nucleotides and index mapping
CHARACTERS = ["A", "C", "G", "T", "-"]
idx = {nt:i for i,nt in enumerate(CHARACTERS)}

# Build cost matrix (default = 2.5, transitions = 1, identity = 0)
cost_mat = np.full((5, 5), 2.5)
cost_mat[idx['A'], idx['G']] = cost_mat[idx['G'], idx['A']] = 1.0
cost_mat[idx['C'], idx['T']] = cost_mat[idx['T'], idx['C']] = 1.0
# Gap to everything else is 5
cost_mat[:, idx["-"]] = 5
cost_mat[idx["-"], :] = 5
np.fill_diagonal(cost_mat, 0.0)


print("The Cost Matrix:")
print(cost_mat)


def init_tip_seq(tree, tip_name, observed_seq):
    """
    Generalized version of init_tip.
    Each node has a 5 by 1 by n matrix
    """
    n = len(observed_seq)
    mat = np.full((5, 1, n), np.inf)  # fill with np.inf
    for j, nt in enumerate(observed_seq):
        if nt in idx:
            mat[idx[nt], 0, j] = 0
        else:
            raise Exception(f"Unknown character: {nt}")
    tree.nodes[tip_name]['matrix'] = mat
    return None

def sankoff_calculate_seq(cost_matrix, tree, node_name, seq_len):
    """
    For the specified node of the tree, calculate the minimum possible cost 
    for each nucleotide. 
    """

    children = list(tree.successors(node_name))
    left_mat = tree.nodes[children[0]]['matrix']
    right_mat = tree.nodes[children[1]]['matrix']

    # Add the third axis to cost matrix
    cost_mat_seq = np.reshape(cost_matrix, shape=(5, 5, 1))
    # Repeat cost matrix n times, from 5 by 5 by 1 to 5 by 5 by n
    cost_mat_repeat = np.repeat(cost_mat_seq, seq_len, axis = 2)

    # Repeat the child matrix to make it fit the shape of cost matrix
    # Repeat the vector across rows, from 5 by 1 by n to 5 by 5 by n
    child_mat_1 = np.repeat(left_mat, 5, axis = 1)
    child_mat_1 += cost_mat_repeat
    child_mat_2 = np.repeat(right_mat, 5, axis = 1)
    child_mat_2 += cost_mat_repeat

    # Get the minimum across each column
    # From 5 by 5 by n to 1 by 5 by n
    child_mat_1 = np.min(child_mat_1, axis = 0, keepdims = True)
    child_mat_2 = np.min(child_mat_2, axis = 0, keepdims = True)
    mat = child_mat_1 + child_mat_2

    # Transpose the matrix, from 1 by 5 back to 5 by 1, swap axes 0 and 1
    tree.nodes[node_name]['matrix'] = np.transpose(mat, axes=(1, 0, 2))
    return None

def sankoff_traverse_seq(c_matrix, tree, node_name, seq_len):
    """
    Traverse the tree recursively, calculating costs for each node.
    Calculate a node's children before the node itself.
    This function depends on correctly initialising the costs in the tips
    of the tree before traversing the tree.
    """
    children = list(tree.successors(node_name))
    if len(children) <= 0:
        return None
    if len(children) != 2:
        raise Exception("Incorrect binary tree")
    left_node = children[0]
    right_node = children[1]
    # Traverse left and right node
    sankoff_traverse_seq(c_matrix, tree, left_node, seq_len)
    sankoff_traverse_seq(c_matrix, tree, right_node, seq_len)
    # Add the matrix if not exist
    if not "matrix" in tree.nodes[node_name]:
        tree.nodes[node_name]["matrix"] = np.zeros((5, seq_len))
    sankoff_calculate_seq(c_matrix, tree, node_name, seq_len)

def calculate_tree_parsimony(msa: dict, tree: nx.DiGraph) -> float:

    # Get the length of the first sequence
    seq_len = len(list(msa.values())[0])
    # Check all sequences share the same length
    for seq in msa.values():
        assert len(seq) == seq_len

    # Initialize the tips with the sequence
    for seq_name in msa.keys():
        seq = msa[seq_name]
        init_tip_seq(tree, seq_name, seq)
    
    sankoff_traverse_seq(cost_mat, tree, "root", seq_len)
    return None


"""
All three trees should have the same score.
Why do they have the same score even if B and C is more similar than A?
A distance-based method would naturally group B and C together.
However, max parsimony (Sankoff) doesn't "cluster".
Instead, it asks for each site, what is the cheapest way to explain these three tip states on a tree?
If two strings are similar, and one is distinct, it would always be one change (one mutation),
no matter how we construct the tree.
"""