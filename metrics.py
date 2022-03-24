class Metric:

    # get path, return a number - lower is better
    def evaluate(self, path):
        return 1

    # get list of paths, returns list sorted by evaluate
    def sort(self, paths, reverse=False):
        return sorted(paths, key=self.evaluate, reverse=reverse)


class ShortestPathMetric(Metric):

    def evaluate(self, path):
        return path.length()


class SafestPathMetric(Metric):
    def __init__(self, omit_first=True, omit_last=True):
        self.omit_first = omit_first
        self.omit_last = omit_last

    def evaluate(self, path):
        return 1 / path.get_min_fatal_distance(self.omit_first, self.omit_last)
