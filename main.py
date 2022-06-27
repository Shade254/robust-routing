import getopt
import math
import os.path
import random

from executor import TestExecutor
from graph import Graph
from graphics import display_instance
from metrics import *
from strategy import DynamicProgrammingStrategy, \
    ShortestPathStrategy, CombinedPathStrategy
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
        opts, args = getopt.getopt(argv, "pshg:d:f:n:l:a:b:",
                                   ["graph=", "direction=", "count=", "length=", "force=", "origin=", "destination=",
                                    "save", "display", "help"])
    except Exception as e:
        print("Cannot load input arguments: " + e.__str__())
        sys.exit(1)

    graph_path = None

    # up, bottom, right, left
    direction = ""

    min_force = 1
    max_force = 1

    od_distance = 10
    od_number = 5

    save = False
    display = False

    a = None
    b = None

    for opt, arg in opts:
        if opt in ['-g', "--graph"]:
            graph_path = arg
        elif opt in ['-d', "--direction"]:
            direction = arg
        elif opt in ['-n', "--count"]:
            od_number = int(arg)
        elif opt in ['-l', "--length"]:
            od_distance = int(arg)
        elif opt in ['-f', "--force"]:
            force = arg.split("-")
            min_force = int(force[0])
            max_force = int(force[1])
        elif opt in ['-s', "--save"]:
            save = True
        elif opt in ['-p', "--display"]:
            display = True
        elif opt in ['-a', "--origin"]:
            a = arg
        elif opt in ['-b', "--destination"]:
            b = arg
        elif opt in ['-h', "--help"]:
            print("Usage:")
            print("-g, --graph: path to txt file with graph (required)")
            print("-d, --direction: direction of possible disturbances (default - ubrl [means up, "
                  "bottom, right, left])")
            print("-f, --force: minima and maximal force of possible disturbances (default 1-1)")
            print("-n, --count: count of random origin/destination pairs to test (default 5)")
            print("-l, --length: minimal manhattan distance of every origin/destination pair (default 10)")
            print("-a, --origin: origin of a pair to test (format Y:X, has preference over -n and -l)")
            print("-b, --destination: destination of a pair to test (format Y:X, has preference over -n and -l)")
            print("-s, --save: specify this option to save graphical output to ./output folder)")
            print("-d, --display: specify this option to display graphical output on a screen")
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
        display_instance(graph, marking, display=display, save=save, show_numbers=True)

        # ================ RUN TEST =================

        tested_strategies = [
            ShortestPathStrategy(graph, marking),
            CombinedPathStrategy(graph, marking, 1, 6, lambda x: 1 / x, "1:x"),
            # CombinedPathStrategy(graph, marking, 1, 1, lambda x : sinus(x), "sin"),
            DynamicProgrammingStrategy(graph, marking, VectorSafetyMetric(marking)),
            # DynamicProgrammingStrategy(graph, marking, VectorSafetyMetric(marking, 7)),
            # DynamicProgrammingStrategy(graph, marking, SafestPathMetricV1(marking)),
            # DynamicProgrammingStrategy(graph, marking, SafestPathMetricV2(marking)),
        ]
        if a and graph.get_node(a) and b and graph.get_node(b):
            pairs = [(a, b)]
        else:
            pairs = generate_od_pairs(graph, marking, od_number, min_distance=od_distance)
        executor = TestExecutor(graph, marking, tested_strategies, pairs)

        results = executor.execute(show_strategy=True, show_planned=True, show_executed=True, display=display,
                                   save=save)

        output_to_csv(results, graph_path=g, path="raw_results.csv")
