import random

class Dice:
    def __init__(self, numDice, numSides):
        self.numDice = numDice
        self.numSides = numSides

    def roll(self):
        rolls = [random.randint(1, self.numSides) for _ in range(self.numDice)]
        count = sum(rolls)
        dupes = self.numDice == 2 and rolls[0] == rolls[1]
        return count, dupes
