from queue import PriorityQueue


# This implementation returns only cost
# not the complete shortest path (shouldnt be needed for our use-case)
class Dijkstra:

    def __init__(self, graph):
        self.graph = graph

    def run(self, from_id, to_ids, kind_of_edges):
        queue = PriorityQueue()
        queue.put((0, from_id))

        while not queue.empty():
            current_cost, current_id = queue.get()

            if current_id in to_ids:
                return current_cost

            out_edges = self.graph.get_out_edges(current_id, kind_of_edges)
            if out_edges:
                for e in out_edges:
                    queue.put((current_cost + e.cost, e.to_id))

        return None
