import getopt
import sys

from graph import Graph
#to run: ../python.exe ../main.py -g "test_cases/basic.txt"

if __name__ == '__main__':
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "g:")
    except:
        print("Cannot load input arguments")
        sys.exit(1)

    graph_path = None

    for opt, arg in opts:
        if opt in ['-g']:
            graph_path = arg
        elif opt in ['-h']:
            print("Usage:")
            print("-g path to txt file with graph (required)")
            sys.exit(0)

    if not graph_path:
        print("Error: Path to graph required!")
        print("Use -h option to print out usage of the script")
        sys.exit(-1)

    graph = Graph(graph_path)
