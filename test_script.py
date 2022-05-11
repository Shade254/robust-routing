import getopt
from random import random
import sys
from warnings import catch_warnings

from executor import TestExecutor
from graph import Graph
from graph_builder import graph_builder
from graphics import display_instance
from marking import Marking
from metrics import SafestPathMetric, ShortestPathMetric, VectorSafetyMetric
from strategy import DynamicProgrammingStrategy
from utils import generate_od_pairs, output_to_csv
import random

# up, bottom, right, left
direction = "ubrl"
min_force = 1
max_force = 1

for i in range(41, 130):
    graph = Graph(f'test_cases/test_case_{i}.txt')
    
    print('creating disturbance edges')
    graph.create_disturbance_edges(direction, min_force, max_force)
    
    print('Calculating marking')
    marking = Marking(graph)
    
    tested_strategies = []
    print('Building strategies')
    tested_strategies.append(DynamicProgrammingStrategy(graph, marking, ShortestPathMetric()))
    tested_strategies.append(DynamicProgrammingStrategy(graph, marking, SafestPathMetric(marking)))
    tested_strategies.append(DynamicProgrammingStrategy(graph, marking, VectorSafetyMetric(marking)))
    results = ""
    try:
        print('generating pairs')
        pairs = generate_od_pairs(graph, marking, 5, min_distance=14)
        print('Creating test executor')
        executor = TestExecutor(graph, marking, tested_strategies, pairs, 0.2)
        print('Running test')
        results = executor.execute()
    except:
        continue
    print('Writing results')
    output_to_csv(results,'strategies_results.csv')
    