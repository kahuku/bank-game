import random

from bots.Bot import Bot

'''
MedianBot will bank randomly a certain percentage of the time 
AFTER half of the players have banked
according to the parameters below.
'''

class MedianBot(Bot):
    def __init__(self, bankThreshold=.25, playerThreshold=.5):
        super().__init__()
        self.bankThreshold = bankThreshold
        self.playerThreshold = playerThreshold

    def decideBank(self, roundScore, game):
        if len(game.unbankedPlayers) // len(game.players) >= self.playerThreshold:
            return False
        return random.uniform(0, 1) < self.bankThreshold

    def __str__(self):
        return f"MedianBot ({(self.bankThreshold * 100):.0f}, {(self.playerThreshold * 100):.0f})"
