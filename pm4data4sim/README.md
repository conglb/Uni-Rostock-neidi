# PM4Py4Data4Sim - Process Mining Python Package

Condensed refactored version of all numbered scripts from the Data4Sim project.

## Structure

```
pm4py4data4sim/
├── __init__.py           # Package initialization and exports
├── data-processing.py    # Data conversion and preprocessing (00, 01, 02, 07, 08, 09, 092)
├── mining.py            # Process mining algorithms (11, 12, 13, 15, 17, 18)
├── visualization.py     # Visualization functions (20, 22, 23, 25, 26, 27)
├── evaluation.py        # Conformance checking and evaluation (33, 330, 331, 332, 43, 53, 19)
├── graph.py            # Graph utilities (60, 61, 070, 071, 076)
├── algo            # Graph utilities (60, 61, 070, 071, 076)
├── utils            # Shared utilities between all modules (60, 61, 070, 071, 076)
└── README.md           # This documentation
```

## Function Mapping

### Data Processing Module (`data_processing.py`)

| Original Script | Function | Description |
|----------------|----------|-------------|
| `00_convert_data_csv_to_xes.py` | `convert_csv_to_xes_activity()` | Convert activity-only CSV to XES |
| `01_csv_to_xes_activity+location.py` | `convert_csv_to_xes_activity_location()` | Convert activity+location CSV to XES |
| `02_csv_to_xes_remove_merge_activity.py` | `convert_csv_to_xes_activity()` with `remove_activities` | Convert with activity filtering |
| `07_csv_to_xes_all_subjects_*.py` | `convert_csv_to_xes_all_subjects()` | Convert all subjects to single XES |
| `08_csv_to_xes_all_subjects_activity+sublocation.py` | `convert_csv_to_xes_all_subjects()` with `data_format="activity+location"` | Convert with sublocation |
| `09_segment_high_level_process.py` | `label_high_level_process()` | Label high-level processes |
| `092_segment_high_level_process_by_fitness.py` | `segment_high_level_process_by_fitness()` | Segment by fitness with evaluation |

### Mining Module (`mining.py`)

| Original Script | Function | Description |
|----------------|----------|-------------|
| `11_initial_miner_alpha_plus.py` | `mine_process_alpha()` | Alpha algorithm mining |
| `12_initial_miner.py` | `mine_process_inductive()` | Inductive algorithm mining |
| `13_initial_miner_for_subprocess.py` | `mine_process_inductive()` with custom parameters | Subprocess mining |
| `15_init_petrinet_from_multiple_xes.py` | `init_petrinet_from_multiple_xes()` | Multi-XES mining |
| `17_initial miner_high-level_processes.py` | `mine_high_level_processes()` | High-level process mining |
| `18_heutistic-miner.py` | `mine_process_heuristic()` | Heuristic algorithm mining |

### Visualization Module (`visualization.py`)

| Original Script | Function | Description |
|----------------|----------|-------------|
| `20_output.py` | `visualize_petri_net()` | Basic Petri net visualization |
| `22_pnml_to_bpmn_png.py` | `visualize_bpmn()` | BPMN visualization |
| `23_pnml_to_png.py` | `visualize_petri_net()` | PNG export |
| `25_output.py` | `visualize_petri_net()` | Alternative output |
| `26_visualize_without_skip_connections.py` | `visualize_petri_net_without_skip()` | Skip-free visualization |
| `27_colored_petrinet_png.py` | `visualize_colored_petri_net()` | Colored visualization |

### Evaluation Module (`evaluation.py`)

| Original Script | Function | Description |
|----------------|----------|-------------|
| `33_scoring.py` | `check_fitness_token_replay()` | Token replay fitness |
| `330_scoring.py` | `check_fitness_token_replay()` | Alternative scoring |
| `331_calculate_fitness.py` | `check_fitness_token_replay()` | Fitness calculation |
| `332_alignment.py` | `check_fitness_alignment()` | Alignment-based fitness |
| `43_alignment.py` | `check_fitness_alignment()` | Alignment method |
| `53_evaluation.py` | `evaluate_model()` | Comprehensive evaluation |
| `19_clustering.py` | `cluster_processes()` | Process clustering |

### Graph Utils Module (`graph_utils.py`)

| Original Script | Function | Description |
|----------------|----------|-------------|
| `60_convert_petrinet_to_graph.py` | `convert_petri_net_to_graph()` | Petri net to graph conversion |
| `61_graph_analysis.py` | `analyze_graph_structure()` | Graph structure analysis |
| `070_convert_petrinet_to_graph.py` | `convert_petri_net_to_graph()` | Alternative conversion |
| `071_detect_subnet.py` | `detect_subnet()` | Subnet detection |
| `076_convert_graph_to_petrinet.py` | `convert_graph_to_petrinet()` | Graph to Petri net conversion |

## Usage

### Import the package

```python
import pm5py
```

### Data Processing

```python
# Convert CSV to XES (replaces 00_convert_data_csv_to_xes.py)
pm5py.convert_csv_to_xes_activity("data/S01.csv", "results/S01.xes")

# Convert activity+location (replaces 01_csv_to_xes_activity+location.py)
pm5py.convert_csv_to_xes_activity_location(
    "data/S01_Activity.csv",
    "data/S01_Location.csv", 
    "data/S01_Main-Process.csv",
    "results/S01.xes"
)

# Convert all subjects (replaces 07_csv_to_xes_all_subjects_*.py)
pm5py.convert_csv_to_xes_all_subjects("data/", "results/all_subjects.xes")

# Label high-level processes (replaces 09_segment_high_level_process.py)
import pandas as pd
df = pd.read_csv("data/S01.csv")
df_labeled = pm5py.label_high_level_process(df)
```

### Process Mining

```python
# Alpha Miner (replaces 11_initial_miner_alpha_plus.py)
net, initial_marking, final_marking = pm5py.mine_process_alpha("data.xes", "output.pnml")

# Inductive Miner (replaces 12_initial_miner.py)
net, initial_marking, final_marking = pm5py.mine_process_inductive("data.xes", "output.pnml")

# Heuristic Miner (replaces 18_heutistic-miner.py)
net, initial_marking, final_marking = pm5py.mine_process_heuristic("data.xes", "output.pnml")

# High-level processes (replaces 17_initial miner_high-level_processes.py)
net, marking = pm5py.mine_high_level_processes("data.xes", "output.pnml")
```

### Visualization

```python
# Visualize Petri net (replaces 20_output.py, 23_pnml_to_png.py)
pm5py.visualize_petri_net("model.pnml", "model.png")

# Visualize without skip connections (replaces 26_visualize_without_skip_connections.py)
pm5py.visualize_petri_net_without_skip("model.pnml", "model_clean.png")

# Visualize BPMN (replaces 22_pnml_to_bpmn_png.py)
pm5py.visualize_bpmn("model.pnml", "model.bpmn")

# Colored visualization (replaces 27_colored_petrinet_png.py)
pm5py.visualize_colored_petri_net("model.pnml", "model_colored.png")
```

### Evaluation

```python
# Token replay fitness (replaces 33_scoring.py, 331_calculate_fitness.py)
fitness_results = pm5py.check_fitness_token_replay("log.xes", "model.pnml")

# Alignment fitness (replaces 43_alignment.py)
fitness_results = pm5py.check_fitness_alignment("log.xes", "model.pnml")

# Complete evaluation (replaces 53_evaluation.py)
evaluation_results = pm5py.evaluate_model("log.xes", "model.pnml")

# Clustering (replaces 19_clustering.py)
pm5py.cluster_processes("log.xes", "clusters.json", num_clusters=3)
```

### Graph Utilities

```python
# Convert Petri net to graph (replaces 60_convert_petrinet_to_graph.py)
pm5py.convert_petri_net_to_graph("model.pnml", "model.gml")

# Analyze graph structure (replaces 61_graph_analysis.py)
metrics = pm5py.analyze_graph_structure("model.gml")

# Detect subnets (replaces 071_detect_subnet.py)
pm5py.detect_subnet("model.pnml", "subnets.json")

# Convert graph to Petri net (replaces 076_convert_graph_to_petrinet.py)
pm5py.convert_graph_to_petrinet("model.gml", "model.pnml")
```

## Complete Workflow Example

```python
import pm5py

# 1. Convert CSV to XES (replaces 00_convert_data_csv_to_xes.py)
pm5py.convert_csv_to_xes_activity("data/S01.csv", "results/S01.xes")

# 2. Mine process model (replaces 12_initial_miner.py)
net, initial_marking, final_marking = pm5py.mine_process_inductive("results/S01.xes", "results/S01.pnml")

# 3. Visualize (replaces 20_output.py)
pm5py.visualize_petri_net("results/S01.pnml", "results/S01.png")

# 4. Check fitness (replaces 33_scoring.py)
fitness = pm5py.check_fitness_token_replay("results/S01.xes", "results/S01.pnml")
print(f"Fitness: {fitness['fitness']:.4f}")

# 5. Convert to graph (replaces 60_convert_petrinet_to_graph.py)
pm5py.convert_petri_net_to_graph("results/S01.pnml", "results/S01.gml")

# 6. Analyze graph (replaces 61_graph_analysis.py)
metrics = pm5py.analyze_graph_structure("results/S01.gml")
print(f"Graph metrics: {metrics}")
```

## Dependencies

- `pm4py` - Process mining library
- `pandas` - Data manipulation
- `networkx` - Graph analysis
- `matplotlib` - Visualization
- `scikit-learn` - Clustering and evaluation
- `numpy` - Numerical operations

## Installation

```bash
pip install pm4py pandas networkx matplotlib scikit-learn numpy
```

## Benefits

- **Organized Structure**: Functions grouped by functionality
- **Clear Mapping**: Each function maps to original scripts
- **Easy Migration**: Simple function calls replace script execution
- **Modular Design**: Import only what you need
- **Well Documented**: Clear docstrings and examples
- **Maintainable**: Centralized, organized code

## Migration Guide

### From Original Scripts

**Before:**
```bash
python 00_convert_data_csv_to_xes.py
python 12_initial_miner.py
python 20_output.py
```

**After:**
```python
import pm5py
pm5py.convert_csv_to_xes_activity("data.csv", "output.xes")
net, marking = pm5py.mine_process_inductive("output.xes", "model.pnml")
pm5py.visualize_petri_net("model.pnml", "model.png")
```

This package provides a clean, organized interface for all process mining operations while preserving all the functionality of the original numbered scripts.
