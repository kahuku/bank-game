class Player:
    def __init__(self, name, brain=None, quiet=False):
        self.name = name
        self.score = 0
        self.banked = False
        self.brain = brain
        self.quiet = quiet
        self.roundScores = []

    def __str__(self):
        return f"{self.name} {'(' + self.brain.__str__() + ')' if self.brain else ''} has {self.score} points"

    def decideBank(self, roundScore, game):
        if self.banked:
            return True

        if self.brain:
            bank = self.brain.decideBank(roundScore, game)
        else:
            bank = input(f"{self.name}, do you want to bank {roundScore} points? (y/n): ").lower() == "y"

        self.banked = bank
        if bank:
            self.score += roundScore
            self.roundScores.append(roundScore)
            if not self.quiet:
                print(f"{self.name} banked {roundScore} points")
        
        return self.banked
