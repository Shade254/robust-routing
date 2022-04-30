import random

from marking import Marking
from strategy import Strategy
from graph import EdgeClass, Graph


class Player:
    def take_action(self):
        pass

    def is_at_goal(self) -> bool:
        return False

    def set_current_position(self, pos):
        pass

    def current_position(self):
        pass


class NormalPlayer(Player):
    def __init__(self, strategy: Strategy, graph: Graph, marking: Marking, start, goal):
        self.current = start
        self.goal = goal
        self.graph = graph
        self.marking = marking
        self.strategy = strategy
        self.current_path = self.strategy.get_full_path(start, goal)

    def take_action(self):
        move = self.strategy.get_move(self.current_position())
        self.set_current_position(move.to_id)
        return move

    def is_at_goal(self) -> bool:
        return self.current == self.goal

    def current_position(self):
        return self.current

    def set_current_position(self, pos):
        self.current = pos


class ProbabilisticDisturbancePlayer(Player):
    def __init__(self, player: Player, graph: Graph, probability):
        self.player = player
        self.graph = graph
        self.probability = probability

    def take_action(self):
        current = self.player.current_position()
        intended_action = self.player.take_action()

        dis = self.graph.get_out_edges(current, EdgeClass.DISTURBANCE)
        has_disturbance = len(dis) > 0

        option = random.uniform(0, 1)
        if has_disturbance and option <= self.probability:
            disturbances_move = random.choice(dis)
            self.player.set_current_position(disturbances_move.to_id)
            return disturbances_move

        return intended_action

    def is_at_goal(self) -> bool:
        return self.player.is_at_goal()
