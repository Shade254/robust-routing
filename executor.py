from graphics import display_instance
from path import Path
from player import MaliciousDisturbancePlayer, NormalPlayer, \
    ProbabilisticDisturbancePlayer


class TestExecutor:
    def __init__(self, graph, marking, strategies, od_pairs):
        self.graph = graph
        self.marking = marking
        self.strategies = strategies
        self.od_pairs = od_pairs

    def get_dist_players(self, player, graph, marking):
        return [
            ProbabilisticDisturbancePlayer(player, graph, 0.2),
            MaliciousDisturbancePlayer(player, graph, 0.2, marking)
            ]

    def execute(self):
        results = {}
        i = 0
        for o, d in self.od_pairs:
            print(
                str(i) + "/" + str(len(self.od_pairs) - 1) + " Evaluation Origin:" + str(
                    o) + " Destination: " + str(d))
            for s in self.strategies:
                print("Evaluating strategy " + s.__str__())
                if s.__str__() not in results:
                    results[s.__str__()] = {}
                s.build_strategy(d)
                tuple_d = (int(d.split(':')[1]), int(d.split(':')[0]))
                display_instance(self.graph, self.marking, s, None, None, tuple_d,
                                 title=s.__str__())
                player = NormalPlayer(s, self.graph, self.marking, o, d)
                dist_players = self.get_dist_players(player, self.graph, self.marking)
                for dist_player in dist_players:
                    dist_player.reset(o, d)
                    success = True
                    while not player.is_at_goal():
                        try:
                            dist_player.take_action()
                        except:
                            success = False
                            break
                    if dist_player.__str__() not in results[s.__str__()]:
                        results[s.__str__()][dist_player.__str__()] = []
                    results[s.__str__()][dist_player.__str__()].append((
                        o, d, success,
                        Path(player.planned_path, self.graph,
                             self.marking),
                        Path(player.executed_path, self.graph,
                             self.marking)))
            i += 1

        return results
