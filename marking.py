from dijkstra import Dijkstra
from graph import EdgeClass, NodeClass


class Marking:

    def __init__(self, graph):
        self.graph = graph
        self.marking = {}
        self.count_marking()

    def count_marking(self):
        ok_nodes = self.graph.get_all_nodes(NodeClass.OK)
        fatal_nodes = self.graph.get_all_nodes(NodeClass.FATAL)

        for f in ok_nodes:
            dijkstra = Dijkstra(self.graph)
            no_disturbances = dijkstra.run(f, fatal_nodes, EdgeClass.DISTURBANCE)
            self.marking[f] = no_disturbances

    def get_marking(self, node_id):
        if node_id in self.marking:
            return self.marking[node_id]
        return None
