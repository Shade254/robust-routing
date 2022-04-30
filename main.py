import getopt
import sys

from graph import EdgeClass, Graph
from graphics import display_instance
from marking import Marking
from metrics import SafestPathMetric, ShortestPathMetric
from path import Path
import matplotlib.pyplot as plt


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

    # ======== MARKING NODES BY FATAL DISTANCE =========

    marking = Marking(graph)

    # ================ TEST OF METRICS =================

    nodes_path1 = ['2:9', '2:8', '2:7', '2:6', '2:5', '2:4', '2:3', '2:2', '2:1']
    nodes_path2 = ['2:9', '3:9', '3:8', '3:7', '3:6', '3:5', '3:4', '3:3', '3:2', '3:1',
                   '2:1']

    edges_path1 = []
    edges_path2 = []

    for i in range(len(nodes_path1)):
        if i == 0:
            continue
        edges_path1.append(
            graph.get_edge(nodes_path1[i - 1], nodes_path1[i], EdgeClass.NORMAL))

    for i in range(len(nodes_path2)):
        if i == 0:
            continue
        edges_path2.append(
            graph.get_edge(nodes_path2[i - 1], nodes_path2[i], EdgeClass.NORMAL))

    test_path1 = Path(edges_path1, graph, marking)
    test_path2 = Path(edges_path2, graph, marking)

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

    # ================ DISPLAY PATH AND GRAPH =================
    edges_path3 = []
    for e in edges_path2:
        dist_edges = ['2:9', '3:7', '3:6']
        if e.from_id in dist_edges:
            edges_path3.append(graph.get_edge(e.from_id, e.to_id, EdgeClass.DISTURBANCE))
        else:
            edges_path3.append(e)

    while len(edges_path3) > 0:
        test_path3 = Path(edges_path3, graph, marking)
        fig, ax = display_instance(graph, marking, path=test_path3)
        plt.show()
        edges_path3.pop(0)
