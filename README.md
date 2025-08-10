# Data4Sim

## Intro
This repo contains work in process mining from Data4Sim project. The project is joined between university and company. The data is collected from electrical devices and annotators. The objective is to finding the hidden multi-level processes in the log data.

## Organization
00: csv to xes
01: csv to xes
02: name:concept = activity+location
03
04
05

1x: Miner running. Output is PNML files.

2x: Export to PNG, images.

3x:

4x:

5x:

7xx: pipeline for Petrinet transformation
8x: Petrinet/Trace clustering

09: [Phase 1] [S01]
092: Detecting high-level processes (given a Main-Area Petri-Net) [Phase 1] [S02]

6x: Detecting Midle-level processes.


## Running / Pipeline

```
bash ./run.sh
```

```
python 00_convert_data_csv_to_xes.py
python initial_miner.py
python output.py
```

To build Petrinet

```
python 0x.py
python 1x.py
python 20_output.py
```

Middle-level Process Classification

```

```

Detect High-level Process

```
python 08.py
python 17.py
python 092_segment_high_level_process_by_fitness.py
```

To build Graph from PNML
```

```

Detect Midle-level Process.
```
```