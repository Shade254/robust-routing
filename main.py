import getopt
import math
import sys

from executor import TestExecutor
from graph import Graph
from graphics import display_instance
from marking import Marking
from strategy import CombinedPathStrategy
from utils import generate_od_pairs, output_to_csv

if __name__ == '__main__':

    # ============== COMMAND LINE INTERFACE ===============
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hg:d:f:")
    except:
        print("Cannot load input arguments")
        sys.exit(1)

    graph_path = None

    # up, bottom, right, left
    direction = "ubrl"

    min_force = 1
    max_force = 1

    for opt, arg in opts:
        if opt in ['-g']:
            graph_path = arg
        elif opt in ['-d']:
            direction = arg
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

    # ============== CREATING BASE GRAPH ===============

    graph = Graph(graph_path)
    graph.create_disturbance_edges(direction, min_force, max_force)

    print("Loaded %d nodes, %d edges and %d disturbance edges" % (
        len(graph.get_all_nodes()), graph.num_of_normal_edges,
        graph.num_of_disturbance_edges))
    print("Graph dimensions: " + str(graph.max_row) + " x " + str(
        graph.max_column) + "\n\n")

    # ======== MARKING NODES BY FATAL DISTANCE =========

    marking = Marking(graph)

    # ================ RUN TEST =================
    tested_strategies = [
        CombinedPathStrategy(graph, marking, 1, 1, lambda x: 1 / x, "1/x"),
        CombinedPathStrategy(graph, marking, 1, 1, lambda x: 1 / (math.e ** x), "1/e^x")]
    pairs = generate_od_pairs(graph, marking, 5, min_distance=4)
    executor = TestExecutor(graph, marking, tested_strategies, pairs, 0.4)

    results = executor.execute()

    output_to_csv(results)

    for i in range(len(results[tested_strategies[0].__str__()])):
        for s in results.keys():
            display_instance(graph, marking, results[s][i][3])
            display_instance(graph, marking, results[s][i][4])
