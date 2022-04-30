from queue import PriorityQueue

from graph import EdgeClass, Graph
from marking import Marking


class Strategy:
    def __init__(self, graph: Graph, goal_node_id, marking: Marking):
        self.strategy = {}
        self.graph = graph
        self.goal_node = goal_node_id
        self.marking = marking
        self.build_strategy(graph, marking, goal_node_id)

    def get_move(self, node):
        if node in self.strategy:
            return self.strategy[node]
        return None

    def get_full_path(self, start, end):
        path = []
        while len(path) == 0 or path[-1].to_id != end:
            if len(path) == 0:
                edge = self.get_move(start)
            else:
                edge = self.get_move(path[-1].to_id)
            if not edge:
                raise ValueError("Invalid strategy for path from " + start + " to " + end)
            path.append(edge)
        return path

    def build_strategy(self, graph, marking, goal_node_id):
        queue = PriorityQueue()
        queue.put((0, [goal_node_id]))

        while not queue.empty():
            current_value, current_path = queue.get()
            if current_path[-1] not in self.strategy:
                if current_value != 0:
                    self.strategy[current_path[-1]] = graph.get_edge(current_path[-1],
                                                                     current_path[-2],
                                                                     EdgeClass.NORMAL)

                in_edges = self.graph.get_in_edges(current_path[-1], EdgeClass.NORMAL)

                if in_edges:
                    for e in in_edges:
                        queue.put((current_value + self.cost_func(e, marking),
                                   current_path + [e.from_id]))

    def cost_func(self, e, marking):
        return 1


class ShortestPathStrategy(Strategy):
    def cost_func(self, e, marking):
        return e.cost


class CombinedPathStrategy(Strategy):
    def __init__(self, graph: Graph, goal_node_id, marking: Marking, alpha, beta,
                 risk_function):
        super().__init__(graph, goal_node_id, marking)
        self.alpha = alpha
        self.beta = beta
        self.risk_function = risk_function

    def cost_func(self, e, marking):
        risk_value = marking.get_marking(e.to_id)
        if not risk_value:
            risk_value = 0
        return self.alpha * e.cost + self.beta * self.risk_function(risk_value)
