


def get_all_strongly_connected_components(G):
    """
    Get all strongly connected components of a directed graph.
    
    Parameters:
    G (networkx.DiGraph): The directed graph.
    
    Returns:
    list: A list of sets, where each set contains the nodes in a strongly connected component.
    """
    return list(nx.strongly_connected_components(G))

def get_subnet_from_scc(G, scc):
    """
    Get the subgraph corresponding to a strongly connected component (SCC). 
    """
    return G.subgraph(scc).copy()  # extract the subgraph of the SCC

def get_subnet_from_sccs(G, sccs):
    """
    Get the subnets corresponding to all strongly connected components (SCCs).
    """
    subnets = []
    for scc in sccs:
        subnet = get_subnet_from_scc(G, scc)
        subnets.append(subnet)
    return subnets

def get_subnet_from_sccs_as_dict(G, sccs):
    """
    Get the subnets corresponding to all strongly connected components (SCCs) as a dictionary.
    """
    subnets = {}
    for i, scc in enumerate(sccs):
        subnet = get_subnet_from_scc(G, scc)
        subnets[f"SCC_{i}"] = subnet
    return subnets