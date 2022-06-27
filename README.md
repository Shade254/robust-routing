# Computing and visualizing robust plans

This project aims to provide a functional framework for implementation, evaluation and visualization of strategies used
to generate robust plans to move an agent in a non-deterministic environment.

## Command line interface

- `-g, --graph`: path to text file with graph
- `-d, --direction`: direction of disturbances in the graph (e.g. `ublr` - up, bottom, left, right)
- `-f, --force`: force interval of disturbances (e.g. `1-3` - disturbances with force 1, 2 and 3, default `1-1`)
- `-n, --count`: count of random origin/destination pairs to test (default 5)
- `-l, --length`: minimal manhattan distance of every origin/destination pair (default 10)
- `-a, --origin`: origin of a pair to test (format `Y:X`, has preference over `-n` and `-l`)
- `-b, --destination`: destination of a pair to test (format `Y:X`, has preference over `-n` and `-l`)
- `-s, --save`: specify this option to save graphical output to `./output` folder
- `-p, --display`: specify this option to display graphical output on a screen
- `-h, --help`: print out available options

## Graph format

Graph is loaded from a text file. Graphs should be specified in a grid format. Format examples are shown
in `./test_cases`
folder.

- `.` - safe node
- `x` - fatal node
- ` ` (space) - wall

## Metrics and strategies

Strategies used to construct the optimal paths for a problem instance are defined in `main.py` file
field `tested_strategies`. Each OD pair will be evaluated using these strategies and executed against all specified
disturbance players (see below). The output is both text and graphical. The text output is stored in `raw_results.csv`
file and its format is defined by the header row. Each consecutive row is then an information about single execution.

Strategies are built using metrics. All metrics for dynamical programming computed strategies are implemented
in `metrics.py` file. To create a new metric just extend `Metric` interface from this file and insert the resulting
class in a `DynamicProgramming` object. Strategies computed with a Dijkstra algorithm don't require any extra
implementation. Just specify your cost function and insert it into new `CombinedPathStrategy` object.

## Disturbance agents

Disturbance agents are used to pick and trigger disturbances during the execution of the strategy. Agents used in the
evaluation are stored in file `executor.py` in a method `get_dist_players`. Their interface and specific implementations
are coded in `player.py`.