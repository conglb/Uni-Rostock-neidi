import networkx as nx

def remove_skip_edges(G: nx.DiGraph):
    """
    Remove nodes from a directed graph whose name (node attribute 'name' or the node itself if a string)
    starts with 'skip'.
    """
    nodes_to_remove = []

    for node in G.nodes:
        # Get the node name: if node is a string, use it; otherwise, try G.nodes[node]['name']
        node_name = None
        if isinstance(node, str):
            node_name = node
        elif 'name' in G.nodes[node]:
            node_name = G.nodes[node]['name']
        
        if node_name and node_name.startswith("skip"):
            nodes_to_remove.append(node)

    # Remove nodes (this automatically removes connected edges in a DiGraph)
    G.remove_nodes_from(nodes_to_remove)