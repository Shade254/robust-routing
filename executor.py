from graphics import display_instance
from path import Path
from player import NormalPlayer, ProbabilisticDisturbancePlayer


class TestExecutor:
    def __init__(self, graph, marking, strategies, od_pairs, probability):
        self.graph = graph
        self.marking = marking
        self.strategies = strategies
        self.od_pairs = od_pairs
        self.probability = probability

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
                    results[s.__str__()] = []
                s.build_strategy(d)
                tuple_d = (int(d.split(':')[1]), int(d.split(':')[0]))
                display_instance(self.graph, self.marking, s, None, None, tuple_d,
                                 title=s.__str__())
                player = NormalPlayer(s, self.graph, self.marking, o, d)
                dist_player = ProbabilisticDisturbancePlayer(player, self.graph,
                                                             self.probability)

                success = True
                while not player.is_at_goal():
                    try:
                        dist_player.take_action()
                    except:
                        success = False
                        break

                results[s.__str__()].append((o, d, success,
                                             Path(player.planned_path, self.graph,
                                                  self.marking),
                                             Path(player.executed_path, self.graph,
                                                  self.marking)))
            i += 1

        return results
