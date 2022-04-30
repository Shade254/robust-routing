import getopt
import sys

from graph import Graph, NodeClass
from graphics import display_instance
from marking import Marking
from metrics import ShortestPathMetric
from path import Path
from player import NormalPlayer, ProbabilisticDisturbancePlayer
from strategy import Strategy

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

    # ================ TEST OF Strategy =================
    start = "5:5"
    goal = "1:1"
    goal_pos = (int(goal.split(":")[0]),
           int(goal.split(":")[1]))
    probability = 0.2
    strategy = Strategy(graph, goal, marking)

    player = NormalPlayer(strategy, graph, marking, start, goal)
    disturbance = ProbabilisticDisturbancePlayer(player, graph, probability)

    succes = True

    actualPath = []

    while not player.is_at_goal():
        if graph.get_node(player.current_position()).kind == NodeClass.FATAL:
            succes = False
            break
        next_edge = disturbance.take_action()
        actualPath.append(next_edge)
        path = Path(actualPath, graph, marking)
        pos = (int(player.current_position().split(":")[1]), int(player.current_position().split(":")[0]))
        display_instance(graph, marking, path, pos, goal_pos)

    if succes:
        print("Robot got to goal in " + str(len(actualPath)) + " moves")
        print(ShortestPathMetric().evaluate(path))
    else:
        print("FATALITY")




