from bots.Bot import Bot

'''
ExpectedBot will bank when the round score hits the expected value passed in (by default, the average score per round)
'''

class ExpectedBot(Bot):
    def __init__(self, expectation=97):
        super().__init__()
        self.expectation = expectation

    def decideBank(self, roundScore, game):
        return roundScore >= self.expectation

    def __str__(self):
        return f"ExpectedBot ({self.expectation})"
