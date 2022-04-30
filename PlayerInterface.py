import random

from marking import Marking
from path_generator import PathGenerator
from graph import EdgeClass, Graph, Node, NodeClass


class Player:
    def take_action(self):
        pass

    def is_at_goal(self) -> bool:
        return False

    def set_current_position(self, pos):
        pass

    def current_position(self):
        pass


class PlayerPath(Player):
    def __init__(self, path_generator: PathGenerator, graph: Graph, marking: Marking, current, goal, ):
        self.current = current
        self.goal = goal
        self.graph = graph
        self.marking = marking
        self.pathGenerator = path_generator
        self.currentPath = self.pathGenerator.current_path.path_edges

    def take_action(self):
        if self.current not in self.currentPath:
            print(self.current)
            self.pathGenerator.build_path(self.graph, self.goal, self.current, self.marking)
            self.currentPath = self.pathGenerator.current_path.path_edges

        path = self.currentPath
        self.currentPath.pop(0)
        if len(self.currentPath) > 0:
            self.set_current_position(self.currentPath[0].to_id)
        return path

    def is_at_goal(self) -> bool:
        return self.current == self.goal

    def current_position(self):
        return self.current

    def set_current_position(self, pos):
        self.current = pos


class DisturbancePlayer(Player):
    def __init__(self, player: Player, graph: Graph):
        self.player = player
        self.graph = graph

    def take_action(self):
        current = self.player.current_position()
        dis = self.graph.get_in_edges(current, EdgeClass.DISTURBANCE)
        has_disturbance = len(dis) > 0

        intended_action = self.player.take_action()

        option = random.uniform(0, 1)
        if has_disturbance and option <= 0.2:
            disturbances_move = random.choice(dis)
            self.player.set_current_position(disturbances_move.from_id)
            return self.player.take_action()

        return intended_action

    def is_at_goal(self) -> bool:
        return self.player.is_at_goal()
