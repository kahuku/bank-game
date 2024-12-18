import random

from bots.Bot import Bot

'''
DumbBot will bank randomly a certain percentage of the time according to the parameters below.
'''

class DumbBot(Bot):
    def __init__(self, bankThreshold=.25):
        super().__init__()
        self.bankThreshold = bankThreshold

    def decideBank(self, roundScore, game):
        return random.uniform(0, 1) < self.bankThreshold

    def __str__(self):
        return f"DumbBot ({(self.bankThreshold * 100):.0f})"
