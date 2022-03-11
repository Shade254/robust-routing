from queue import PriorityQueue

from graph import EdgeClass, NodeClass


class Marking:

    def __init__(self, graph):
        self.graph = graph
        self.marking = {}
        self.count_marking()

    def count_marking(self):
        fatal_nodes = self.graph.get_all_nodes(NodeClass.FATAL)
        queue = PriorityQueue()

        for f in fatal_nodes:
            queue.put((0, f))

        while not queue.empty():
            current_value, current_node = queue.get()
            if current_node not in self.marking:
                if current_value != 0:
                    self.marking[current_node] = current_value

                in_edges = self.graph.get_in_edges(current_node, EdgeClass.DISTURBANCE)

                if in_edges:
                    for e in in_edges:
                        queue.put((current_value + 1, e.from_id))

    def get_marking(self, node_id):
        if node_id in self.marking:
            return self.marking[node_id]
        return None
