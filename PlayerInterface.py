class Player:
    def setStrategy(self, strategy):
        pass

    def setDestinations(self, goal):
        pass

    def takeAction(self):
        pass

    def isAtGoal(self) -> bool:
        return False


class PlayerPath(Player):
    def __init__(self, path):
        self.path = path

    def takeAction(self):
        current = self.path
        self.path.pop()

        return current

    def isAtGoal(self) -> bool:
        return len(self.path) == 1
