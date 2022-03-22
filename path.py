class Path:
    # Shouldn't we store edges instead? This way we dont know if we took regular or
    # disturbance edge between two nodes

    def __init__(self, node_ids_array, graph, marking):
        self.path_nodes = node_ids_array
        self.path_marking = []

        self.__graph = graph
        self.__graph_marking = marking

        for n in node_ids_array:
            if not self.__graph.get_node(n):
                raise ValueError("Node " + n + " on the path is not in the graph")
            m = self.__graph_marking.get_marking(n)
            if not m:
                m = float('inf')
            self.path_marking.append(m)

    def __str__(self):
        return "PATH: " + str(self.path_nodes)

    # sometimes we dont want to consider first and last nodes, because they are the
    # same for every path in the set
    @staticmethod
    def __get_list_without_ends(orig_list, omit_first=False, omit_last=False):
        if omit_first:
            orig_list = orig_list[1:]
        if omit_last:
            orig_list = orig_list[:-1]
        return orig_list

    def length(self, omit_first=False, omit_last=False):
        return len(self.__get_list_without_ends(self.path_nodes, omit_first, omit_last))

    def get_max_fatal_distance(self, omit_first=False, omit_last=False):
        return max(self.__get_list_without_ends(self.path_marking, omit_first, omit_last))

    def get_min_fatal_distance(self, omit_first=False, omit_last=False):
        return min(self.__get_list_without_ends(self.path_marking, omit_first, omit_last))

    def get_avg_fatal_distance(self, omit_first=False, omit_last=False):
        edited_list = self.__get_list_without_ends(self.path_marking, omit_first,
                                                   omit_last)
        return sum(edited_list) / len(edited_list)

    def get_nth_node(self, n):
        return self.__graph.get_node(self.path_nodes[n])

    def get_all_nodes(self):
        nodes = []
        for i in range(len(self.path_nodes)):
            nodes.append(self.get_nth_node(i))
        return nodes