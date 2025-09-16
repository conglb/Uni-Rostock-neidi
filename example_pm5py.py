#!/usr/bin/env python3
"""
Example usage of the PM5Py package
Demonstrates the condensed refactored functions
"""

import pm4py4data4sim
import os
from pathlib import Path

def example_data_processing():
    """Data processing examples"""
    print("=== Data Processing Examples ===")
    
    # Ensure directories exist
    Path("results").mkdir(exist_ok=True)
    
    # Example 1: Convert CSV to XES (replaces 00_convert_data_csv_to_xes.py)
    print("1. Converting CSV to XES...")
    pm4py4data4sim.convert_csv_to_xes_activity(
        "data/S01.csv", 
        "results/S01.xes",
        case_id="Case_01",
        remove_activities=['Standing', 'Synchronization']
    )
    
    # Example 2: Convert activity+location (replaces 01_csv_to_xes_activity+location.py)
    print("2. Converting activity+location...")
    pm4py4data4sim.convert_csv_to_xes_activity_location(
        "data/S01_Activity.csv",
        "data/S01_Location.csv",
        "data/S01_Main-Process.csv",
        "results/S01_activity_location.xes",
        process_filter="Retrieval"
    )
    
    # Example 3: Convert all subjects (replaces 07_csv_to_xes_all_subjects_*.py)
    print("3. Converting all subjects...")
    pm4py4data4sim.convert_csv_to_xes_all_subjects(
        "data/",
        "results/all_subjects.xes",
        data_format="activity"
    )
    
    print("Data processing examples completed!")


def example_mining():
    """Process mining examples"""
    print("\n=== Process Mining Examples ===")
    
    # Example 1: Alpha Miner (replaces 11_initial_miner_alpha_plus.py)
    print("1. Alpha Miner...")
    net_alpha, marking_alpha = pm4py4data4sim.mine_process_alpha("results/S01.xes", "results/S01_alpha.pnml")
    
    # Example 2: Inductive Miner (replaces 12_initial_miner.py)
    print("2. Inductive Miner...")
    net_inductive, marking_inductive = pm4py4data4sim.mine_process_inductive("results/S01.xes", "results/S01_inductive.pnml")
    
    # Example 3: Heuristic Miner (replaces 18_heutistic-miner.py)
    print("3. Heuristic Miner...")
    net_heuristic, marking_heuristic = pm4py4data4sim.mine_process_heuristic("results/S01.xes", "results/S01_heuristic.pnml")
    
    # Example 4: High-level processes (replaces 17_initial miner_high-level_processes.py)
    print("4. High-level processes...")
    net_high, marking_high = pm4py4data4sim.mine_high_level_processes("results/S01.xes", "results/S01_high_level.pnml")
    
    print("Process mining examples completed!")


def example_visualization():
    """Visualization examples"""
    print("\n=== Visualization Examples ===")
    
    # Example 1: Basic visualization (replaces 20_output.py, 23_pnml_to_png.py)
    print("1. Basic Petri net visualization...")
    pm4py4data4sim.visualize_petri_net("results/S01_inductive.pnml", "results/S01_basic.png")
    
    # Example 2: Without skip connections (replaces 26_visualize_without_skip_connections.py)
    print("2. Without skip connections...")
    pm4py4data4sim.visualize_petri_net_without_skip("results/S01_inductive.pnml", "results/S01_no_skip.png")
    
    # Example 3: BPMN visualization (replaces 22_pnml_to_bpmn_png.py)
    print("3. BPMN visualization...")
    pm4py4data4sim.visualize_bpmn("results/S01_inductive.pnml", "results/S01.bpmn")
    
    # Example 4: Colored visualization (replaces 27_colored_petrinet_png.py)
    print("4. Colored visualization...")
    color_map = {"transition1": "red", "transition2": "blue"}
    pm4py4data4sim.visualize_colored_petri_net("results/S01_inductive.pnml", "results/S01_colored.png", color_map)
    
    print("Visualization examples completed!")


def example_evaluation():
    """Evaluation examples"""
    print("\n=== Evaluation Examples ===")
    
    # Example 1: Token replay fitness (replaces 33_scoring.py, 331_calculate_fitness.py)
    print("1. Token replay fitness...")
    fitness_token = pm4py4data4sim.check_fitness_token_replay("results/S01.xes", "results/S01_inductive.pnml")
    print(f"   Token replay fitness: {fitness_token['fitness']:.4f}")
    
    # Example 2: Alignment fitness (replaces 43_alignment.py, 332_alignment.py)
    print("2. Alignment fitness...")
    fitness_align = pm4py4data4sim.check_fitness_alignment("results/S01.xes", "results/S01_inductive.pnml")
    print(f"   Alignment fitness: {fitness_align['fitness']:.4f}")
    
    # Example 3: Complete evaluation (replaces 53_evaluation.py)
    print("3. Complete evaluation...")
    evaluation_results = pm4py4data4sim.evaluate_model("results/S01.xes", "results/S01_inductive.pnml")
    print(f"   Evaluation results: {evaluation_results}")
    
    # Example 4: Clustering (replaces 19_clustering.py)
    print("4. Process clustering...")
    pm4py4data4sim.cluster_processes("results/S01.xes", "results/clusters.json", num_clusters=3)
    
    print("Evaluation examples completed!")


def example_graph_utils():
    """Graph utilities examples"""
    print("\n=== Graph Utilities Examples ===")
    
    # Example 1: Convert Petri net to graph (replaces 60_convert_petrinet_to_graph.py, 070_convert_petrinet_to_graph.py)
    print("1. Converting Petri net to graph...")
    pm4py4data4sim.convert_petri_net_to_graph("results/S01_inductive.pnml", "results/S01.gml")
    
    # Example 2: Analyze graph structure (replaces 61_graph_analysis.py)
    print("2. Analyzing graph structure...")
    metrics = pm4py4data4sim.analyze_graph_structure("results/S01.gml")
    print(f"   Graph metrics: {metrics}")
    
    # Example 3: Detect subnets (replaces 071_detect_subnet.py)
    print("3. Detecting subnets...")
    pm4py4data4sim.detect_subnet("results/S01_inductive.pnml", "results/subnets.json")
    
    # Example 4: Convert graph to Petri net (replaces 076_convert_graph_to_petrinet.py)
    print("4. Converting graph to Petri net...")
    pm4py4data4sim.convert_graph_to_petrinet("results/S01.gml", "results/S01_from_graph.pnml")
    
    print("Graph utilities examples completed!")


def example_high_level_process_detection():
    """High-level process detection example"""
    print("\n=== High-Level Process Detection Example ===")
    
    import pandas as pd
    
    # Create sample data
    sample_data = {
        'Main Area': ['Base', 'Aisle path', 'Cross aisle path', 'Office'],
        'Sub-Location': ['Start', 'Middle', 'End', 'Finish'],
        'Activity': ['Scan', 'Tick off / confirm', 'Tick off / confirm', 'Complete']
    }
    df = pd.DataFrame(sample_data)
    
    # Label high-level processes (replaces 09_segment_high_level_process.py)
    print("1. Labeling high-level processes...")
    df_labeled = pm4py4data4sim.label_high_level_process(df)
    print("   High-level process labels added!")
    
    # Save results
    df_labeled.to_csv("results/sample_labeled.csv", index=False)
    print("   Results saved to results/sample_labeled.csv")
    
    # Segment by fitness (replaces 092_segment_high_level_process_by_fitness.py)
    print("2. Segmenting by fitness...")
    pm4py4data4sim.segment_high_level_process_by_fitness(
        "data/S01.csv",
        "results/S01_segmented.csv",
        "results/S01_preprocessed.csv",
        "results/S01_predicted.csv"
    )
    
    print("High-level process detection completed!")


def example_complete_workflow():
    """Complete workflow example"""
    print("\n=== Complete Workflow Example ===")
    
    # This demonstrates the typical workflow from the original scripts
    
    # Step 1: Convert CSV to XES (replaces 00_convert_data_csv_to_xes.py)
    print("Step 1: Converting CSV to XES...")
    pm4py4data4sim.convert_csv_to_xes_activity("data/S01.csv", "results/workflow_S01.xes")
    
    # Step 2: Mine process model (replaces 12_initial_miner.py)
    print("Step 2: Mining process model...")
    net, initial_marking, final_marking = pm4py4data4sim.mine_process_inductive("results/workflow_S01.xes", "results/workflow_S01.pnml")
    
    # Step 3: Visualize (replaces 20_output.py)
    print("Step 3: Visualizing...")
    pm4py4data4sim.visualize_petri_net("results/workflow_S01.pnml", "results/workflow_S01.png")
    
    # Step 4: Check fitness (replaces 33_scoring.py)
    print("Step 4: Checking fitness...")
    fitness = pm4py4data4sim.check_fitness_token_replay("results/workflow_S01.xes", "results/workflow_S01.pnml")
    print(f"   Fitness: {fitness['fitness']:.4f}")
    
    # Step 5: Convert to graph (replaces 60_convert_petrinet_to_graph.py)
    print("Step 5: Converting to graph...")
    pm4py4data4sim.convert_petri_net_to_graph("results/workflow_S01.pnml", "results/workflow_S01.gml")
    
    # Step 6: Analyze graph (replaces 61_graph_analysis.py)
    print("Step 6: Analyzing graph...")
    metrics = pm4py4data4sim.analyze_graph_structure("results/workflow_S01.gml")
    print(f"   Graph metrics: {metrics}")
    
    print("Complete workflow example finished!")


def main():
    """Main function to run all examples"""
    print("PM5Py Package - Example Usage")
    print("=============================")
    
    # Check if data directory exists
    if not Path("data").exists():
        print("Warning: 'data' directory not found. Some examples may fail.")
        print("Please ensure you have the required data files in the 'data' directory.")
        return
    
    try:
        # Run examples
        example_data_processing()
        example_mining()
        example_visualization()
        example_evaluation()
        example_graph_utils()
        example_high_level_process_detection()
        example_complete_workflow()
        
        print("\n" + "="*50)
        print("All PM5Py examples completed successfully!")
        print("Check the 'results' directory for output files.")
        print("\nFunction mapping summary:")
        print("- Data Processing: 00, 01, 02, 07, 08, 09, 092 -> data_processing.py")
        print("- Mining: 11, 12, 13, 15, 17, 18 -> mining.py")
        print("- Visualization: 20, 22, 23, 25, 26, 27 -> visualization.py")
        print("- Evaluation: 33, 330, 331, 332, 43, 53, 19 -> evaluation.py")
        print("- Graph Utils: 60, 61, 070, 071, 076 -> graph_utils.py")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Please ensure you have the required data files and dependencies installed.")


if __name__ == "__main__":
    main()
