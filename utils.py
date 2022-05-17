import os
import random
import sys

from graph import NodeClass
from path import Path


def generate_od_pairs(graph, marking, count, min_distance=2, min_risk=1,
                      max_risk=sys.maxsize):
    pairs = []
    all_nodes = graph.get_all_nodes(NodeClass.OK)
    for i in range(count):
        while True:
            from_node = random.choice(all_nodes)
            from_risk = marking.get_marking(from_node)
            if not from_risk:
                from_risk = sys.maxsize

            if min_risk <= from_risk <= max_risk:
                break

        while True:
            to_node = random.choice(all_nodes)
            to_risk = marking.get_marking(to_node)

            if not to_risk:
                to_risk = sys.maxsize

            if min_risk >= to_risk >= max_risk:
                continue

            distance_y = abs(
                int(from_node.split(':')[0]) - int(to_node.split(':')[0]))
            distance_x = abs(
                int(from_node.split(':')[1]) - int(to_node.split(':')[1]))

            if (distance_x + distance_y) >= min_distance:
                break

        pairs.append((from_node, to_node))
    return pairs


def output_to_csv(results, graph_path="UNKNOWN", path="output.csv"):
    existing = os.path.exists(path)
    with open(path, "a") as f:
        if not existing:
            f.write(
                "Graph,Name,Function,Alpha,Beta,Start,End,DisturbancePlayer,Success,PlannedPath,PlannedPathMarking,ExecutedPath,ExecutedPathMarking\n")
        for k in results.keys():
            for d, v in results[k].items():
                for row in v:
                    str = graph_path + ',' + k
                    for entry in row:
                        if not isinstance(entry, Path):
                            if isinstance(entry, bool):
                                str += "," + d + "," + entry.__str__()
                            else:
                                str += "," + entry.__str__()
                        else:
                            str += ","
                            for n in entry.path_nodes:
                                str += n + "-"
                            str = str[:-1]
                            str += ","
                            for n in entry.path_marking:
                                str += n.__str__() + "-"
                            str = str[:-1]
                    str += '\n'
                    f.write(str)


def get_edge_direction(edge):
    from_id = [int(x) for x in edge.from_id.split(':')]
    to_id = [int(x) for x in edge.to_id.split(':')]

    vector = [from_id[i] - to_id[i] for i in range(len(from_id))]

    if vector == [-1, 0]:
        return 'b'
    elif vector == [1, 0]:
        return 'u'
    elif vector == [0, -1]:
        return 'r'
    elif vector == [0, 1]:
        return 'l'
    return None


def get_succes_rate(list_of_bool):
    sum = 0
    for i in list_of_bool:
        if i:
            sum += 1

    return sum / len(list_of_bool)


# A function that calculates numbers of pairs in a string
# Each pair is separated by a '-'
def get_number_of_pairs(string):
    return len(string.split("-"))


# average of a string of numbers
# each number is separated by a '-'
def get_avg_marking(string):
    list_of_numbers = string.split("-")
    sum = 0
    for i in list_of_numbers:
        if i != 'inf':
            sum += int(i)
    return sum / len(list_of_numbers)


# calculate the manhatten distance between two points
# points written as X:Y
def get_manhattan_distance(point1, point2):
    x1 = int(point1.split(":")[0])
    y1 = int(point1.split(":")[1])
    x2 = int(point2.split(":")[0])
    y2 = int(point2.split(":")[1])
    return abs(x1 - x2) + abs(y1 - y2)


# convert decimal value to percentage in string format
def get_percentage(value,round_to=4):
    return str(round(value * 100,round_to)) + "%"


def get_length_difference(string_path1, string_path2):
    return len(string_path1.split("-")) - len(string_path2.split("-"))
