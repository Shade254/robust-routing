import os
import random
import sys
import time

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
            if min_risk <= from_risk <= max_risk:
                break

        while True:
            to_node = random.choice(all_nodes)
            to_risk = marking.get_marking(to_node)

            if min_risk > to_risk > max_risk:
                continue

            distance_y = abs(
                int(from_node.split(':')[0]) - int(to_node.split(':')[0]))
            distance_x = abs(
                int(from_node.split(':')[1]) - int(to_node.split(':')[1]))

            if (distance_x + distance_y) >= min_distance:
                break

        pairs.append((from_node, to_node))
    return pairs


def output_to_csv(results):
    for k, v in results.items():
        time_stamp = time.strftime("%b_%d_%Y_%H_%M", time.localtime())
        filename = k.split(",")[0] + "_" + time_stamp + ".csv"
        existing = os.path.exists(filename)
        with open(filename, "a") as f:
            if not existing:
                f.write(
                    "Name,Function,Alpha,Beta,Start,End,Success,PlannedPath,PlannedPathMarking,ExecutedPath,ExecutedPathMarking\n")
            for row in v:
                str = k
                for entry in row:
                    if not isinstance(entry, Path):
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


def get_succes_rate(list_of_bool):
    sum = 0
    for i in list_of_bool:
        if i:
            sum += 1

    return sum / len(list_of_bool)


def get_length_difference(string_path1, string_path2):
    return len(string_path1.split("-")) - len(string_path2.split("-"))