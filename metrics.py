import collections
import sys


class Metric:
    def choose(self, path1, path2):
        pass


class ShortestPathMetric(Metric):
    def choose(self, path1, path2):
        if len(path1) < len(path2):
            return path1
        return path2

    def __str__(self):
        return "ShortestLength"


class MarkingMetric(Metric):
    def __init__(self, marking):
        self.marking = marking

    def _get_markings(self, path, use_from=False):
        markings = []
        if use_from:
            m = self.marking.get_marking(path[0].from_id)
            if not m:
                m = sys.maxsize
            markings.append(m)

        for p in path:
            m = self.marking.get_marking(p.to_id)
            if not m:
                m = sys.maxsize
            markings.append(m)
        return markings


class VectorSafetyMetric(MarkingMetric):
    def __init__(self, marking, cutoff=None):
        super().__init__(marking)
        self.cutoff = cutoff

    def choose(self, path1, path2):
        markings1 = self._get_markings(path1)
        markings2 = self._get_markings(path2)

        vector1 = collections.Counter(markings1)
        vector2 = collections.Counter(markings2)

        if self.cutoff:
            if self.cutoff not in vector1:
                vector1[self.cutoff] = 0
            if self.cutoff not in vector2:
                vector2[self.cutoff] = 0
            to_remove = []
            for k, v in vector1.items():
                if k > self.cutoff:
                    vector1[self.cutoff] += v
                    to_remove.append(k)
            for k in to_remove:
                vector1.pop(k)
            to_remove = []
            for k, v in vector2.items():
                if k > self.cutoff:
                    vector2[self.cutoff] += v
                    to_remove.append(k)
            for k in to_remove:
                vector2.pop(k)

        enums = list(vector1.keys())
        enums.extend(list(vector2.keys()))
        enums = set(enums)

        for i in enums:
            if (i in vector2 and i not in vector1) or vector1[i] < vector2[i]:
                return path1
            elif (i in vector1 and i not in vector2) or vector2[i] < vector1[i]:
                return path2

        return path1

    def __str__(self):
        name = "VectorSafePath"
        if self.cutoff:
            name += "Cut" + str(self.cutoff)
        return name


class SafestPathMetric(MarkingMetric):
    def __init__(self, marking, use_from):
        super().__init__(marking)
        self.use_from = use_from

    def choose(self, path1, path2):
        markings1 = self._get_markings(path1, use_from=self.use_from)
        markings2 = self._get_markings(path2, use_from=self.use_from)

        if min(markings1) > min(markings2):
            return path1
        elif min(markings2) > min(markings1):
            return path2
        else:
            if len(path1) < len(path2):
                return path1
            else:
                return path2


class SafestPathMetricV1(SafestPathMetric):
    def __init__(self, marking):
        super().__init__(marking, use_from=True)

    def __str__(self):
        return "SafestPathV1"


class SafestPathMetricV2(SafestPathMetric):
    def __init__(self, marking):
        super().__init__(marking, use_from=False)

    def __str__(self):
        return "SafestPathV2"
