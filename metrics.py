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


class VectorSafetyMetric(Metric):
    def __init__(self, marking):
        self.marking = marking

    def choose(self, path1, path2):
        markings1 = []
        markings2 = []
        for p in path1:
            m = self.marking.get_marking(p.to_id)
            if not m:
                m = sys.maxsize
            markings1.append(m)

        for p in path2:
            m = self.marking.get_marking(p.to_id)
            if not m:
                m = sys.maxsize
            markings2.append(m)

        vector1 = collections.Counter(markings1)
        vector2 = collections.Counter(markings2)

        enums = list(vector1.keys())
        enums.extend(list(vector2.keys()))
        enums = set(enums)

        for i in enums:
            if (i in vector1 and i not in vector2) or vector1[i] < vector2[i]:
                return path1
            elif (i in vector2 and i not in vector1) or vector2[i] < vector1[i]:
                return path2

        return path1

    def __str__(self):
        return "VectorSafePath"


class SafestPathMetric(Metric):
    def __init__(self, marking):
        self.marking = marking

    def choose(self, path1, path2):
        markings1 = []
        markings2 = []
        for p in path1:
            m = self.marking.get_marking(p.to_id)
            if not m:
                m = sys.maxsize
            markings1.append(m)

        for p in path2:
            m = self.marking.get_marking(p.to_id)
            if not m:
                m = sys.maxsize
            markings2.append(m)

        if min(markings1) > min(markings2):
            return path1
        elif min(markings2) > min(markings1):
            return path2
        else:
            if len(path1) < len(path2):
                return path1
            else:
                return path2

    def __str__(self):
        return "SafestPath"
