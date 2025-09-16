"""
PM4Py4Data4Sim - Process Mining Python Package for Data4Sim
Condensed refactored version of all numbered scripts
"""

from .data_processing import *
from .algo.mining import *
from .visualization import *
from .algo.evaluation import *
from .algo.graph import *

__version__ = "1.0.0"
__author__ = "Data4Sim Team"

__all__ = [
    # Data Processing
    "convert_csv_to_xes_activity",
    "convert_csv_to_xes_activity_location", 
    "convert_csv_to_xes_all_subjects",
    "label_high_level_process",
    "segment_high_level_process_by_fitness",
    
    # Mining
    "mine_process_alpha",
    "mine_process_inductive",
    "mine_process_heuristic",
    "mine_high_level_processes",
    "init_petrinet_from_multiple_xes",
    
    # Visualization
    "visualize_petri_net",
    "visualize_petri_net_without_skip",
    "visualize_bpmn",
    "visualize_colored_petri_net",
    
    # Evaluation
    "check_fitness_token_replay",
    "check_fitness_alignment",
    "evaluate_model",
    "cluster_processes",
    
    # Graph Utils
    "convert_petri_net_to_graph",
    "analyze_graph_structure",
    "detect_subnet",
    "convert_graph_to_petrinet",
    "remove_skip_connections"
]