from marking import Marking
from path_generator import PathGenerator
from graph import EdgeClass, Graph,Node, NodeClass

class Player:
    def setStrategy(self, strategy):
        pass

    def setDestinations(self, goal):
        pass

    def takeAction(self):
        pass

    def isAtGoal(self) -> bool:
        return False


class PlayerPath(Player):

    def __init__(self, pathGenerator: PathGenerator, graph: Graph, marking: Marking, current, goal, ):
        self.current = current
        self.goal = goal
        self.graph = graph
        self.marking = marking
        self.pathGenerator = pathGenerator
        self.currentPath = self.pathGenerator.current_path.path_edges
        print(self.currentPath)

    def takeAction(self):
        self.currentPath.pop(0)
        return self.currentPath

    def isAtGoal(self) -> bool:
        return self.current == self.goal
