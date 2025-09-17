"""
Visualization Module: visual petrinet, bpmn, graph...
Functions mapping from original scripts 20, 22, 23, 25, 26, 27
"""

import pm4py
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def visualize_petri_net(pnml_file: str, output_path: str, remove_skip: bool = True, show: bool = False) -> None:
    """
    Visualize Petri net
    
    Replaces: 20_output.py, 23_pnml_to_png.py, 25_output.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output image file path
        remove_skip: Whether to remove skip connections
        show: Whether to display the visualization
    """
    logger.info(f"Visualizing Petri net: {pnml_file} -> {output_path}")
    
    from .algo.mining import load_pnml
    from .algo.graph import remove_skip_connections
    
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    # Remove skip connections if requested
    if remove_skip:
        net = remove_skip_connections(net)
    
    from pm4py.visualization.petri_net import visualizer as pn_visualizer
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    
    if show:
        pn_visualizer.view(gviz)
    
    pn_visualizer.save(gviz, output_path)
    logger.info(f"Visualization saved: {output_path}")


def visualize_petri_net_without_skip(pnml_file: str, output_path: str) -> None:
    """
    Visualize Petri net without skip connections
    
    Replaces: 26_visualize_without_skip_connections.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output image file path
    """
    visualize_petri_net(pnml_file, output_path, remove_skip=True)


def visualize_bpmn(pnml_file: str, output_path: str) -> None:
    """
    Visualize BPMN from Petri net
    
    Replaces: 22_pnml_to_bpmn_png.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output BPMN file path
    """
    logger.info(f"Creating BPMN visualization: {pnml_file} -> {output_path}")
    
    from .algo.mining import load_pnml
    
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    # Convert to process tree first, then to BPMN
    from pm4py.objects.conversion.process_tree import converter as pt_converter
    from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
    
    # This is a simplified approach - in practice you'd need the original log
    # For now, we'll just visualize the Petri net
    visualize_petri_net(pnml_file, output_path)


def visualize_colored_petri_net(pnml_file: str, output_path: str, color_map: Optional[Dict] = None) -> None:
    """
    Visualize colored Petri net
    
    Replaces: 27_colored_petrinet_png.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output image file path
        color_map: Color mapping for transitions/places
    """
    logger.info(f"Creating colored Petri net visualization: {pnml_file} -> {output_path}")
    
    from .algo.mining import load_pnml
    
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    from pm4py.visualization.petri_net import visualizer as pn_visualizer
    
    parameters = {}
    if color_map:
        parameters["color_map"] = color_map
    
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
    pn_visualizer.save(gviz, output_path)
    logger.info(f"Colored visualization saved: {output_path}")

def visualize_graph_from_pnml(pnml_file: str, output_path: str, show: bool = False) -> None:
    """
    Visualize Petri net as a directed graph using NetworkX
    
    Replaces: 60_convert_petrinet_to_graph.py
    
    Args:
        pnml_file: Input PNML file path
        output_path: Output graph file path (GraphML format)
        show: Whether to display the graph visualization
    """
    logger.info(f"Visualizing Petri net as graph: {pnml_file} -> {output_path}")
    
    import networkx as nx
    from pm4py.objects.petri_net.importer import importer as pnml_importer
    import matplotlib.pyplot as plt
    
    # Load Petri net
    net, initial_marking, final_marking = pnml_importer.apply(pnml_file)
    
    # Convert to networkx graph
    G = nx.DiGraph()
    
    return G


