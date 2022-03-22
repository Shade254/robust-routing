import getopt
import sys

from graph import Graph
from graphics import display_marking_grid
from marking import Marking
from metrics import SafestPathMetric, ShortestPathMetric
from path import Path

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
    display_marking_grid(graph, marking)

    # ================ TEST OF METRICS =================

    nodes_path1 = ['2:9', '2:8', '2:7', '2:6', '2:5', '2:4', '2:3', '2:2', '2:1']
    nodes_path2 = ['2:9', '3:9', '3:8', '3:7', '3:6', '3:5', '3:4', '3:3', '3:2', '3:1',
                   '2:1']

    test_path1 = Path(nodes_path1, graph, marking)
    test_path2 = Path(nodes_path2, graph, marking)

    shortest_metric = ShortestPathMetric()
    safest_metric = SafestPathMetric()

    sorted_shortest = shortest_metric.sort([test_path1, test_path2])
    sorted_safest = safest_metric.sort([test_path2, test_path1])

    print("\n\nShortest metric:")
    for p in sorted_shortest:
        print(p)
        print("VAlUE: " + str(shortest_metric.evaluate(p)))

    print("\n\nSafest metric:")
    for p in sorted_safest:
        print(p)
        print("VAlUE: " + str(safest_metric.evaluate(p)))
