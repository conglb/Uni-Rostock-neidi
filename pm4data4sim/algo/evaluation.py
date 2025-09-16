"""
Evaluation Module
Functions mapping from original scripts 33, 330, 331, 332, 43, 53, 19
"""

import pm4py
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import json
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

# PETRINET EVALUATION

def check_fitness_token_replay(xes_file: str, pnml_file: str) -> Dict[str, float]:
    """
    Check fitness using token replay
    
    Replaces: 33_scoring.py, 330_scoring.py, 331_calculate_fitness.py
    
    Args:
        xes_file: Input XES file path
        pnml_file: Input PNML file path
        
    Returns:
        Dictionary with fitness metrics
    """
    logger.info(f"Checking fitness: {xes_file} vs {pnml_file}")
    
    from .mining import load_pnml
    
    log = pm4py.read_xes(xes_file)
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
    
    total_traces = len(replayed_traces)
    fitting_traces = sum(1 for trace in replayed_traces if trace['trace_fitness'] == 1.0)
    fitness = fitting_traces / total_traces if total_traces > 0 else 0.0
    
    return {
        'fitness': fitness,
        'fitting_traces': fitting_traces,
        'total_traces': total_traces
    }


def check_fitness_alignment(xes_file: str, pnml_file: str) -> Dict[str, float]:
    """
    Check fitness using alignment
    
    Replaces: 43_alignment.py, 332_alignment.py
    
    Args:
        xes_file: Input XES file path
        pnml_file: Input PNML file path
        
    Returns:
        Dictionary with fitness metrics
    """
    logger.info(f"Checking fitness with alignment: {xes_file} vs {pnml_file}")
    
    from .mining import load_pnml
    
    log = pm4py.read_xes(xes_file)
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    from pm4py.algo.conformance.alignments import algorithm as alignments
    alignments_result = alignments.apply(log, net, initial_marking, final_marking)
    
    total_traces = len(alignments_result)
    total_cost = sum(alignment['cost'] for alignment in alignments_result)
    total_optimal_cost = sum(alignment['optimal_cost'] for alignment in alignments_result)
    
    fitness = 1.0 - (total_cost / total_optimal_cost) if total_optimal_cost > 0 else 1.0
    
    return {
        'fitness': fitness,
        'total_cost': total_cost,
        'total_optimal_cost': total_optimal_cost,
        'total_traces': total_traces
    }


def evaluate_model(xes_file: str, pnml_file: str) -> Dict[str, float]:
    """
    Comprehensive model evaluation
    
    Replaces: 53_evaluation.py
    
    Args:
        xes_file: Input XES file path
        pnml_file: Input PNML file path
        
    Returns:
        Dictionary with evaluation metrics
    """
    logger.info(f"Evaluating model: {xes_file} vs {pnml_file}")
    
    results = {}
    
    # Fitness
    fitness_results = check_fitness_token_replay(xes_file, pnml_file)
    results.update(fitness_results)
    
    # Load model for additional metrics
    from .mining import load_pnml
    net, initial_marking, final_marking = load_pnml(pnml_file)
    
    # Simplicity (based on model size)
    results['simplicity'] = 1.0 / (len(net.places) + len(net.transitions)) if (len(net.places) + len(net.transitions)) > 0 else 0.0
    
    logger.info("Model evaluation completed")
    return results


def cluster_processes(xes_file: str, output_path: str, num_clusters: int = 3) -> None:
    """
    Cluster processes
    
    Replaces: 19_clustering.py
    
    Args:
        xes_file: Input XES file path
        output_path: Output clustering results file path
        num_clusters: Number of clusters
    """
    logger.info(f"Clustering processes: {xes_file}")
    
    log = pm4py.read_xes(xes_file)
    
    # Simple clustering based on trace length and activity diversity
    trace_features = []
    for trace in log:
        features = [
            len(trace),  # Trace length
            len(set(event['concept:name'] for event in trace))  # Activity diversity
        ]
        trace_features.append(features)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(trace_features)
    
    # Save clustering results
    clustering_results = {
        'num_clusters': num_clusters,
        'cluster_labels': cluster_labels.tolist(),
        'cluster_centers': kmeans.cluster_centers_.tolist()
    }
    
    with open(output_path, 'w') as f:
        json.dump(clustering_results, f, indent=2)
    
    logger.info(f"Clustering completed: {num_clusters} clusters")
