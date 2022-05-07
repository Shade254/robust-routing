import sys
from queue import PriorityQueue

from graph import EdgeClass, Graph, NodeClass
from marking import Marking


class Strategy:
    def __init__(self, graph: Graph, marking: Marking):
        self.strategy = {}
        self.graph = graph
        self.marking = marking

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

    def build_strategy(self, goal_node_id):
        pass


class RoutingStrategy(Strategy):
    def __init__(self, graph: Graph, marking: Marking):
        super().__init__(graph, marking)

    def build_strategy(self, goal_node_id):
        if not goal_node_id:
            return
        self.strategy = {}
        queue = PriorityQueue()
        queue.put((0, [goal_node_id]))

        while not queue.empty():
            current_value, current_path = queue.get()
            if current_path[-1] not in self.strategy:
                if current_value != 0:
                    self.strategy[current_path[-1]] = self.graph.get_edge(
                        current_path[-1],
                        current_path[-2],
                        EdgeClass.NORMAL)

                in_edges = self.graph.get_in_edges(current_path[-1], EdgeClass.NORMAL)

                if in_edges:
                    for e in in_edges:
                        if self.graph.get_node(e.from_id).kind == NodeClass.OK:
                            queue.put((current_value + self.cost_func(e, self.marking),
                                       current_path + [e.from_id]))

    def cost_func(self, e, marking):
        return 1


class DynamicProgrammingStrategy(Strategy):
    def __init__(self, graph, marking, metric):
        super().__init__(graph, marking)
        self.metric = metric

    def build_strategy(self, goal_node_id):
        interim_result = {goal_node_id: (0, [])}

        round = 1
        while True:
            to_process = []
            for k, v in interim_result.items():
                if v[0] == round - 1:
                    to_process.append(k)
            print(to_process)
            if len(to_process) == 0:
                break

            for k in to_process:
                in_edges = self.graph.get_in_edges(k, EdgeClass.NORMAL)
                for n in in_edges:
                    neighbour = n.from_id
                    if self.graph.get_node(neighbour).kind == NodeClass.FATAL:
                        continue
                    new_path = interim_result[k][1].copy()
                    new_path.insert(0, n)

                    old_path = None
                    if neighbour in interim_result:
                        old_path = interim_result[neighbour][1]

                    chosen_path = new_path
                    if old_path:
                        chosen_path = self.metric.choose(new_path, old_path)
                    if chosen_path == new_path:
                        interim_result[neighbour] = (round, chosen_path)
            round += 1
        for k, v in interim_result.items():
            self.strategy[k] = interim_result[k][1][0]

    def __str__(self):
        return "DynamicProgrammingStrategy," + self.metric.__str__()


class ShortestPathStrategy(RoutingStrategy):
    def cost_func(self, e, marking):
        return e.cost

    def __str__(self):
        return "ShortestPathStrategy"


class CombinedPathStrategy(RoutingStrategy):
    def __init__(self, graph: Graph, marking: Marking, alpha, beta,
                 risk_function, risk_function_name="UNKNOWN"):
        super().__init__(graph, marking)
        self.alpha = alpha
        self.beta = beta
        self.risk_function = risk_function
        self.risk_function_name = risk_function_name

    def cost_func(self, e, marking):
        risk_value = marking.get_marking(e.to_id)
        if not risk_value:
            return sys.maxsize
        return self.alpha * e.cost + self.beta * self.risk_function(risk_value)

    def __str__(self):
        return "CombinedPathStrategy," + self.risk_function_name + "," + str(
            self.alpha) + "," + str(self.beta)
