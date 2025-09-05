import networkx as nx
import pandas as pd 

##################
# Introduction 2 #
##################

# undirected
graphA = nx.Graph()
graphA.add_edge('A','B')
graphA.add_edge('A','C')
graphA.add_edge('B','C')
graphA.add_edge('C','D')

# directed
graphB = nx.DiGraph()
graphB.add_edge('A','B')
graphB.add_edge('A','C')
graphB.add_edge('C','B')
graphB.add_edge('C','D')
graphB.add_edge('E','C')

##############
# Exercise 1 #
##############

def degree_distribution(graph):
    """
    For the networkx graph provided, return a dictionary, where
    the keys are all observed vertex degrees, and values are 
    the corresponding counts.
    """
    # basic dict solution
    degree_counts = {}
    for node in graph.nodes():
        degree = graph.degree(node)
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1
    return degree_counts       
    
    # defaultdict(int) solution
    degree_counts = {}
    for node in graph.nodes():
        degree_counts[graph.degree(node)] += 1
    return degree_counts       

    # Counter solution
    from collections import Counter
    degrees = [graph.degree(n) for n in graph.nodes()]
    return Counter(degrees)


###########################
# Exercise 2, challenge 1 #
###########################

density = nx.density(ppi)
gcc = nx.average_clustering(ppi)
apl = nx.average_shortest_path_length(ppi)
n_comps = len(list(nx.connected_components(ppi)))

print(f"Graph density:          {density}")
print(f"Clustering coefficient: {gcc}")
print(f"Average path length:    {apl}")
print(f"Number of Components:   {n_comps}")


###########################
# Exercise 2, challenge 2 #
###########################

# create a dataframe to store metrics for each node
df = pd.DataFrame(index=list(ppi.nodes()))
df['degree'] = nx.degree_centrality(ppi)
df['eigenvector'] = nx.eigenvector_centrality(ppi)
df['betweenness'] = nx.betweenness_centrality(ppi)

# add columns for ranks
df['degree_rank'] = df['degree'].rank(ascending=False, method='min').astype(int)
df['eigenvector_rank'] = df['eigenvector'].rank(ascending=False, method='min').astype(int)
df['betweenness_rank'] = df['betweenness'].rank(ascending=False, method='min').astype(int)

# print out values
query = 'Q0010'
print(f"degree centrality:      {df.loc[query, 'degree']:.3f}, rank={df.loc[query, 'degree_rank']}")
print(f"eigenvector centrality: {df.loc[query, 'eigenvector']:.3f}, rank={df.loc[query, 'eigenvector_rank']}")
print(f"betweenness centrality: {df.loc[query, 'betweenness']:.3f}, rank={df.loc[query, 'betweenness_rank']}")
