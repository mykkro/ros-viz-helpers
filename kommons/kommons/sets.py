# Useful dictionary-like sets for counting occurrences, etc.

class DictWrapper(object):
    def __init__(self):
        self.map = {}

    def put(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError
    
    def __len__(self):
        return len(self.map)

    def items(self):
        return self.map.items()


# Dictionary of sets
class SetDict(DictWrapper):

    def put(self, key, value):
        if key not in self.map:
            self.map[key] = set()
        self.map[key].add(value)

    def get(self, key):
        return self.map.get(key, set())


# Dictionary of lists
class ListDict(DictWrapper):

    def put(self, key, value):
        if key not in self.map:
            self.map[key] = []
        self.map[key].append(value)

    def get(self, key):
        return self.map.get(key, [])


# Dictionary of dicts
class DictDict(DictWrapper):

    def put(self, key, key2, value):
        if key not in self.map:
            self.map[key] = {}
        self.map[key][key2] = value

    def get(self, key, key2=None):
        obj = self.map.get(key, {})
        if key2 is not None:
            obj = obj.get(key2)
        return obj


# Dictionary of counters
class CountingDict(DictWrapper):

    def add(self, key):
        if key not in self.map:
            self.map[key] = 0
        self.map[key] += 1

    def get(self, key):
        return self.map.get(key, 0)
    
    def ratios(self):
        sum = 0
        for key in sorted(self.map):
            sum += self.map[key]
        return [(key, self.map[key]/sum) for key in sorted(self.map)]


# Dictionary of dictionaries of counters
class DictOfCountingDicts(DictWrapper):

    def put(self, key, value):
        if key not in self.map:
            self.map[key] = CountingDict()
        self.map[key].add(value)

    def get(self, key):
        return self.map.get(key, CountingDict())

