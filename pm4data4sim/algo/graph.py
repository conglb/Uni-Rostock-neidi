"""
Graph Utilities Module
Functions mapping from original scripts 60, 61, 070, 071, 076
"""

import networkx as nx
import pm4py
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)

def read_graph_from_gml(gml_file: str) -> nx.DiGraph:
    """
    Read graph from GML file
    
    Args:
        gml_file: Input GML file path
    Returns:
        NetworkX directed graph
    """
    G = nx.read_gml(gml_file)
    logger.info(f"Graph read from {gml_file} with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def write_graph_to_gml(G: nx.DiGraph, output_path: str) -> None:
    """
    Write graph to GML file
    
    Args:
        G: NetworkX directed graph
        output_path: Output GML file path
    """
    nx.write_gml(G, output_path)
    logger.info(f"Graph written to {output_path}")


def remove_skip_connections(net) -> Any:
    """
    Remove skip connections from Petri net
    
    Args:
        net: PM4Py Petri net
        
    Returns:
        Petri net with skip connections removed
    """
    logger.info("Removing skip connections")
    
    nodes_to_remove = []
    
    for place in net.places:
        if place.name and place.name.startswith("skip"):
            nodes_to_remove.append(place)
    
    for transition in net.transitions:
        if transition.label and transition.label.startswith("skip"):
            nodes_to_remove.append(transition)
    
    # Remove nodes
    for node in nodes_to_remove:
        for arc in list(node.in_arcs):
            net.remove_arc(arc)
        for arc in list(node.out_arcs):
            net.remove_arc(arc)
        
        if node in net.places:
            net.places.remove(node)
        if node in net.transitions:
            net.transitions.remove(node)
    
    return net


def convert_petri_net_to_graph(pnml_file: str, output_gml: str) -> None:
    """
    Convert Petri net to graph
    
    Replaces: 60_convert_petrinet_to_graph.py, 070_convert_petrinet_to_graph.py
    
    Args:
        pnml_file: Input PNML file path
        output_gml: Output GML file path
    """
    logger.info(f"Converting Petri net to graph: {pnml_file} -> {output_gml}")
    
    from .mining import load_pnml
    
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    G = nx.DiGraph()
    
    # Add places as nodes
    for place in net.places:
        G.add_node(place.name, type='place', marking=initial_marking.get(place, 0))
    
    # Add transitions as nodes
    for transition in net.transitions:
        G.add_node(transition.name, type='transition', label=transition.label)
    
    # Add arcs as edges
    for arc in net.arcs:
        source = arc.source.name
        target = arc.target.name
        G.add_edge(source, target, weight=1)
    
    nx.write_gml(G, output_gml)
    logger.info(f"Graph exported: {output_gml}")


def analyze_graph_structure(gml_file: str) -> Dict[str, Any]:
    """
    Analyze graph structure
    
    Replaces: 61_graph_analysis.py
    
    Args:
        gml_file: Input GML file path
        
    Returns:
        Dictionary with graph metrics
    """
    logger.info(f"Analyzing graph structure: {gml_file}")
    
    G = nx.read_gml(gml_file)
    
    metrics = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_connected': nx.is_weakly_connected(G),
        'num_components': nx.number_weakly_connected_components(G),
        'average_clustering': nx.average_clustering(G.to_undirected()) if G.number_of_nodes() > 0 else 0
    }
    
    # Add degree statistics
    if G.number_of_nodes() > 0:
        degrees = dict(G.degree())
        metrics['avg_degree'] = sum(degrees.values()) / len(degrees)
        metrics['max_degree'] = max(degrees.values())
        metrics['min_degree'] = min(degrees.values())
    
    logger.info(f"Graph analysis completed: {metrics['num_nodes']} nodes, {metrics['num_edges']} edges")
    return metrics


def detect_subnet(pnml_file: str, output_path: str) -> None:
    """
    Detect subnet in Petri net
    
    Replaces: 071_detect_subnet.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output subnet information file path
    """
    logger.info(f"Detecting subnet: {pnml_file}")
    
    from .mining import load_pnml
    
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    # Simple subnet detection based on strongly connected components
    G = nx.DiGraph()
    
    # Add transitions as nodes
    for transition in net.transitions:
        G.add_node(transition.name)
    
    # Add arcs as edges
    for arc in net.arcs:
        if hasattr(arc.source, 'name') and hasattr(arc.target, 'name'):
            source = arc.source.name
            target = arc.target.name
            G.add_edge(source, target)
    
    # Find strongly connected components
    scc = list(nx.strongly_connected_components(G))
    
    # Save subnet information
    subnet_info = {
        'num_subnets': len(scc),
        'subnets': [list(component) for component in scc]
    }
    
    with open(output_path, 'w') as f:
        json.dump(subnet_info, f, indent=2)
    
    logger.info(f"Detected {len(scc)} subnets")


def convert_graph_to_petrinet(gml_file: str, output_pnml: str) -> None:
    """
    Convert graph to Petri net
    
    Replaces: 076_convert_graph_to_petrinet.py
    
    Args:
        gml_file: Input GML file path
        output_pnml: Output PNML file path
    """
    logger.info(f"Converting graph to Petri net: {gml_file} -> {output_pnml}")
    
    G = nx.read_gml(gml_file)
    
    # Create Petri net from graph
    from pm4py.objects.petri_net.obj import PetriNet, Marking
    from pm4py.objects.petri_net.utils import petri_utils
    
    net = PetriNet()
    initial_marking = Marking()
    final_marking = Marking()
    
    # Add places and transitions based on graph structure
    for node in G.nodes():
        if G.nodes[node].get('type') == 'place':
            place = petri_utils.add_place(net, name=node)
            if G.nodes[node].get('marking', 0) > 0:
                initial_marking[place] = G.nodes[node]['marking']
        elif G.nodes[node].get('type') == 'transition':
            transition = petri_utils.add_transition(net, name=node, label=G.nodes[node].get('label', node))
    
    # Add arcs based on edges
    for edge in G.edges():
        source_name, target_name = edge
        source_node = None
        target_node = None
        
        # Find source and target nodes
        for place in net.places:
            if place.name == source_name:
                source_node = place
                break
        for transition in net.transitions:
            if transition.name == source_name:
                source_node = transition
                break
        
        for place in net.places:
            if place.name == target_name:
                target_node = place
                break
        for transition in net.transitions:
            if transition.name == target_name:
                target_node = transition
                break
        
        if source_node and target_node:
            petri_utils.add_arc_from_to(source_node, target_node, net)
    
    # Save Petri net
    from .mining import save_pnml
    save_pnml(net, initial_marking, final_marking, output_pnml)
    logger.info(f"Graph converted to Petri net: {output_pnml}")
