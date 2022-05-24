from graphics import display_instance
from path import Path
from player import MaliciousDisturbancePlayer, NormalPlayer, \
    PeriodicDisturbancePlayer, ProbabilisticDisturbancePlayer


class TestExecutor:
    def __init__(self, graph, marking, strategies, od_pairs):
        self.graph = graph
        self.marking = marking
        self.strategies = strategies
        self.od_pairs = od_pairs

    def get_dist_players(self, player, graph, marking):
        return [
            ProbabilisticDisturbancePlayer(player, graph, 0.2),
            ProbabilisticDisturbancePlayer(player, graph, 0.5),
            MaliciousDisturbancePlayer(player, graph, 0.2, marking),
            PeriodicDisturbancePlayer(player, graph, 5, -1)
            ]

    def execute(self, show_strategy=False, show_planned=False, show_executed=False,
                save=False, display=False):
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
                if show_strategy:
                    display_instance(self.graph, self.marking, strategy=s, path=None,
                                     position=None, goal=d, save=save, display=display)
                    player = NormalPlayer(s, self.graph, self.marking, o, d)
                    dist_players = self.get_dist_players(player, self.graph, self.marking)

                    planned = Path(player.planned_path, self.graph,
                                   self.marking)

                    if show_planned:
                        display_instance(self.graph, self.marking,
                                         path=planned, goal=d,
                                         display=display, save=save,
                                         strategy_name=s.name)

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
                        executed = Path(player.executed_path, self.graph,
                                        self.marking)
                        results[s.__str__()][dist_player.__str__()].append(
                            (o, d, success, planned, executed))

                        if show_executed:
                            display_instance(self.graph, self.marking, path=executed,
                                             goal=d,
                                             display=display, save=save,
                                             strategy_name=s.name,
                                             dist_name=dist_player.name)
            i += 1

        return results
