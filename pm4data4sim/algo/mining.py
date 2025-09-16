"""
Process Mining Module
Functions mapping from original scripts 11, 12, 13, 15, 17, 18
"""

import pm4py
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def mine_process_alpha(xes_file: str, output_pnml: Optional[str] = None) -> Tuple[Any, Any, Any]:
    """
    Mine process model using Alpha algorithm
    
    Replaces: 11_initial_miner_alpha_plus.py
    
    Args:
        xes_file: Input XES file path
        output_pnml: Output PNML file path (optional)
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Mining process from {xes_file} using Alpha algorithm")
    
    log = pm4py.read_xes(xes_file)
    parameters = {
        "timestamp_key": "time:timestamp",
        "activity_key": "concept:name",
        "case_id_key": "case:concept:name",
        "noise_threshold": 0.0000001
    }
    
    from pm4py.algo.discovery.alpha import algorithm as alpha_miner
    net, initial_marking, final_marking = alpha_miner.apply(log, parameters=parameters)
    
    if output_pnml:
        save_pnml(net, initial_marking, final_marking, output_pnml)
    
    logger.info(f"Mined model: {len(net.places)} places, {len(net.transitions)} transitions")
    return net, initial_marking, final_marking


def mine_process_inductive(xes_file: str, output_pnml: Optional[str] = None, noise_threshold: float = 0.2) -> Tuple[Any, Any, Any]:
    """
    Mine process model using Inductive Miner
    
    Replaces: 12_initial_miner.py, 13_initial_miner_for_subprocess.py
    
    Args:
        xes_file: Input XES file path
        output_pnml: Output PNML file path (optional)
        noise_threshold: Noise threshold for inductive miner
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Mining process from {xes_file} using Inductive algorithm")
    
    log = pm4py.read_xes(xes_file)
    parameters = {
        "timestamp_key": "time:timestamp",
        "activity_key": "concept:name",
        "case_id_key": "case:concept:name",
        "noise_threshold": noise_threshold
    }
    
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    process_tree = inductive_miner.apply(log, parameters=parameters)
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)
    
    if output_pnml:
        save_pnml(net, initial_marking, final_marking, output_pnml)
    
    logger.info(f"Mined model: {len(net.places)} places, {len(net.transitions)} transitions")
    return net, initial_marking, final_marking


def mine_process_heuristic(xes_file: str, output_pnml: Optional[str] = None) -> Tuple[Any, Any, Any]:
    """
    Mine process model using Heuristic Miner
    
    Replaces: 18_heutistic-miner.py
    
    Args:
        xes_file: Input XES file path
        output_pnml: Output PNML file path (optional)
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Mining process from {xes_file} using Heuristic algorithm")
    
    log = pm4py.read_xes(xes_file)
    parameters = {
        "timestamp_key": "time:timestamp",
        "activity_key": "concept:name",
        "case_id_key": "case:concept:name",
        "dependency_threshold": 0.99,
        "and_threshold": 0.8,
        "loop_two_threshold": 0.7
    }
    
    from pm4py.algo.discovery.heuristics import algorithm as heuristic_miner
    net, initial_marking, final_marking = heuristic_miner.apply(log, parameters=parameters)
    
    if output_pnml:
        save_pnml(net, initial_marking, final_marking, output_pnml)
    
    logger.info(f"Mined model: {len(net.places)} places, {len(net.transitions)} transitions")
    return net, initial_marking, final_marking

'''
def mine_high_level_processes(xes_file: str, output_pnml: Optional[str] = None) -> Tuple[Any, Any, Any]:
    """
    Mine high-level processes
    
    Replaces: 17_initial miner_high-level_processes.py
    
    Args:
        xes_file: Input XES file path
        output_pnml: Output PNML file path (optional)
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Mining high-level processes from {xes_file}")
    
    log = pm4py.read_xes(xes_file)
    
    # Filter for high-level processes
    filtered_log = pm4py.filter_event_attribute_values(log, "High-Level Process", ["Storage", "Retrieval"])
    
    # Use inductive miner for high-level processes
    return mine_process_inductive(xes_file, output_pnml)


def init_petrinet_from_multiple_xes(xes_files: List[str], output_pnml: str) -> Tuple[Any, Any, Any]:
    """
    Initialize Petri net from multiple XES files
    
    Replaces: 15_init_petrinet_from_multiple_xes.py
    
    Args:
        xes_files: List of XES file paths
        output_pnml: Output PNML file path
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Initializing Petri net from {len(xes_files)} XES files")
    
    # Read and combine all logs
    combined_log = pm4py.objects.log.obj.EventLog()
    
    for xes_file in xes_files:
        log = pm4py.read_xes(xes_file)
        combined_log.extend(log)
    
    # Mine combined process model
    return mine_process_inductive(combined_log, output_pnml)
'''

def save_pnml(net, initial_marking, final_marking, output_path: str) -> None:
    """
    Save Petri net to PNML file
    
    Args:
        net: Petri net
        initial_marking: Initial marking
        final_marking: Final marking
        output_path: Output file path
    """
    logger.info(f"Saving PNML: {output_path}")
    import pm4py.objects.petri_net.exporter as pn_exporter
    pn_exporter.exporter.apply(net, initial_marking, output_path, final_marking)


def load_pnml(input_path: str) -> Tuple[Any, Any, Any]:
    """
    Load Petri net from PNML file
    
    Args:
        input_path: Input PNML file path
        
    Returns:
        Tuple of (net, initial_marking, final_marking)
    """
    logger.info(f"Loading PNML: {input_path}")
    from pm4py.objects.petri_net.importer import importer as petri_importer
    return petri_importer.apply(input_path)
