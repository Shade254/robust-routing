import getopt
import math
import os.path
import random

from executor import TestExecutor
from graph import Graph
from metrics import *
from strategy import DynamicProgrammingStrategy, \
    ShortestPathStrategy
from utils import generate_od_pairs, output_to_csv


def piecewise(x):
    if x < 6:
        return 7 - x
    else:
        return 1


def sinus(x):
    if x < 16:
        return 4 * math.sin(x / 5 + 1.5) + 5

    return 1


if __name__ == '__main__':

    # ============== COMMAND LINE INTERFACE ===============
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hg:d:f:n:l:")
    except:
        print("Cannot load input arguments")
        sys.exit(1)

    graph_path = None

    # up, bottom, right, left
    direction = ""

    min_force = 1
    max_force = 1

    od_distance = 10
    od_number = 5

    for opt, arg in opts:
        if opt in ['-g']:
            graph_path = arg
        elif opt in ['-d']:
            direction = arg
        elif opt in ['-n']:
            od_number = int(arg)
        elif opt in ['-l']:
            od_distance = int(arg)
        elif opt in ['-f']:
            force = arg.split("-")
            min_force = int(force[0])
            max_force = int(force[1])
        elif opt in ['-h']:
            print("Usage:")
            print("-g path to txt file with graph (required)")
            print("-d direction of possible disturbances (default - ubrl [means up, "
                  "bottom, right, left])")
            print("-f minima and maximal force of possible disturbances (default 1-1)")
            sys.exit(0)

    if not graph_path:
        print("Error: Path to graph required!")
        print("Use -h option to print out usage of the script")
        sys.exit(-1)

    graph_paths = [graph_path]
    if os.path.isdir(graph_path):
        graph_paths = [os.path.join(graph_path, x) for x in os.listdir(graph_path)]
    if len(graph_paths) > 1:
        list.sort(graph_paths,
                  key=lambda x: int(x.split("/")[-1].split(".")[-2].split("_")[-1]))
    random.seed(42)

    for g in graph_paths:
        # ============== CREATING BASE GRAPH ===============

        graph = Graph(g)
        graph.create_disturbance_edges(direction, min_force, max_force)

        print("Loaded %d nodes, %d edges and %d disturbance edges" % (
            len(graph.get_all_nodes()), graph.num_of_normal_edges,
            graph.num_of_disturbance_edges))
        print("Graph dimensions: " + str(graph.max_row) + " x " + str(
            graph.max_column) + "\n\n")

        # ======== MARKING NODES BY FATAL DISTANCE =========

        marking = Marking(graph)
        # display_instance(graph, marking)

        # ================ RUN TEST =================

        tested_strategies = [
            ShortestPathStrategy(graph, marking),
            DynamicProgrammingStrategy(graph, marking, VectorSafetyMetric(marking)),
            DynamicProgrammingStrategy(graph, marking, VectorSafetyMetric(marking, 7)),
            ]
        pairs = generate_od_pairs(graph, marking, od_number, min_distance=od_distance)
        executor = TestExecutor(graph, marking, tested_strategies, pairs)

        results = executor.execute(show_strategy=True, show_planned=True, display=False,
                                   save=True)

        output_to_csv(results, graph_path=g, path="raw_results.csv")
