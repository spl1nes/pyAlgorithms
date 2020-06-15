import operator

class PageRank:
    def __init__(self, relations: dict, isUnique: bool = false, damping: float = 0.85):
        self.pageRanks = {}
        self.relations = {}
        self.outgoing = {}
        self.damping = damping

        for key in relations:
            self.outgoing[key] = len(relations[key])

            if key not in self.relations:
                self.relations[key] = []

            for linkTo in relations[key]:
                if linkTo not in self.relations:
                    self.relations[linkTo] = []

                if linkTo not in self.outgoing:
                    self.outgoing[linkTo] = 0

                if isUnique or key not in self.relations[linkTo]:
                    self.relations[linkTo].append(key)

    def calculateRanks(self, iterations: int = 20, startRank: dict = None):
        if startRank is not None:
            self.pageRanks = startRank
        else:
            for key in self.relations:
                self.pageRanks[key] = 0.0

        i = 0
        while i < iterations:
            for key in self.relations:
                PR = 0.0

                for linkFrom in self.relations[key]:
                    PR += self.pageRanks[linkFrom] / self.outgoing[linkFrom]

                self.pageRanks[key] = 1 - self.damping + self.damping * PR


            i += 1

        ranks = self.pageRanks
        return sorted(ranks.items() , reverse=True, key=lambda x: x[1])
