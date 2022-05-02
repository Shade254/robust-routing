import random

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


class ProbabilisticDisturbancePlayer(Player):
    def __init__(self, player: Player, graph: Graph, probability):
        super().__init__()
        self.player = player
        self.graph = graph
        self.probability = probability
        self.planned_path = player.planned_path
        self.executed_path = player.executed_path

    def take_action(self):
        current = self.player._current
        intended_action = self.player.take_action()

        dis = self.graph.get_out_edges(current, EdgeClass.DISTURBANCE)
        has_disturbance = len(dis) > 0

        option = random.uniform(0, 1)
        if has_disturbance and option <= self.probability:
            disturbances_move = random.choice(dis)
            self.player._current = disturbances_move.to_id
            self.player.executed_path[-1] = disturbances_move
            self.planned_path = self.player.executed_path
            return disturbances_move

        self.executed_path = self.player.executed_path
        return intended_action

    def is_at_goal(self) -> bool:
        return self.player.is_at_goal()

    def reset(self, start, goal):
        self.player.reset(start, goal)
        self.planned_path = self.player.planned_path
