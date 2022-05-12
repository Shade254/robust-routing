import random
import sys

from scipy.stats import expon

from graph import EdgeClass, Graph, NodeClass
from marking import Marking
from strategy import Strategy


class Player:
    def __init__(self):
        self._current = None
        self._goal = None
        self.planned_path = None
        self.executed_path = None

    def take_action(self):
        pass

    def is_at_goal(self) -> bool:
        return False

    def reset(self, start, goal):
        pass


class NormalPlayer(Player):
    def __init__(self, strategy: Strategy, graph: Graph, marking: Marking, start, goal):
        super().__init__()
        self.graph = graph
        self.marking = marking
        self.strategy = strategy
        self.reset(start, goal)

    def take_action(self):
        if self.graph.get_node(self._current).kind == NodeClass.FATAL:
            raise ValueError("Cannot take action in FATAL node")
        move = self.strategy.get_move(self._current)
        self.executed_path.append(move)
        self._current = move.to_id
        return move

    def is_at_goal(self) -> bool:
        return self._current and self._goal and self._current == self._goal

    def reset(self, start, goal):
        self._current = start
        self._goal = goal
        self.planned_path = self.strategy.get_full_path(start, goal)
        self.executed_path = []


class DisturbancePlayer(Player):
    def __init__(self, player: Player, graph: Graph):
        super().__init__()
        self.player = player
        self.graph = graph
        self.planned_path = player.planned_path
        self.executed_path = player.executed_path

    def is_at_goal(self) -> bool:
        return self.player.is_at_goal()

    def reset(self, start, goal):
        self.player.reset(start, goal)
        self.planned_path = self.player.planned_path

    def has_disturbance(self, node):
        return len(self.graph.get_out_edges(node, EdgeClass.DISTURBANCE)) > 0

    def should_trigger(self):
        return False

    def pick_disturbance(self, node):
        return random.choice(self.graph.get_out_edges(node, EdgeClass.DISTURBANCE))

    def take_action(self):
        current = self.player._current
        intended_action = self.player.take_action()

        if self.has_disturbance(current) and self.should_trigger():
            disturbance_move = self.pick_disturbance(current)
            self.player._current = disturbance_move.to_id
            self.player.executed_path[-1] = disturbance_move
            self.planned_path = self.player.executed_path
            return disturbance_move

        self.executed_path = self.player.executed_path
        return intended_action


class ProbabilisticDisturbancePlayer(DisturbancePlayer):
    def __init__(self, player: Player, graph: Graph, probability):
        super().__init__(player, graph)
        self.probability = probability

    def should_trigger(self):
        return random.uniform(0, 1) <= self.probability


class ProbabilisticMaliciousDisturbancePlayer(ProbabilisticDisturbancePlayer):
    def __init__(self, player, graph, probability, marking):
        super().__init__(player, graph, probability)
        self.marking = marking

    def pick_disturbance(self, node):
        dist_edges = self.graph.get_out_edges(node, EdgeClass.DISTURBANCE)
        min_robustnes = sys.maxsize
        min_edge = None

        for e in dist_edges:
            if self.graph.get_node(e.to_id).kind == NodeClass.FATAL:
                return e

            robustness = self.marking.get_marking(e.to_id)
            if not robustness:
                robustness = sys.maxsize

            if robustness <= min_robustnes:
                min_robustnes = robustness
                min_edge = e

        return min_edge


class PeriodicDisturbancePlayer(DisturbancePlayer):
    def __init__(self, player, graph, scale=2, loc=0):
        super().__init__(player, graph)
        self.counter = 0
        self.scale = scale
        self.loc = loc

    def should_trigger(self):
        prob = expon.cdf(self.counter, scale=self.scale, loc=self.loc)
        trigger = random.uniform(0, 1) < prob

        if trigger:
            self.counter = 0
        else:
            self.counter += 1

        return trigger
