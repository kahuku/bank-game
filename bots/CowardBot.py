import random

from bots.Bot import Bot

'''
CowardBot will bank every chance it gets
'''

class CowardBot(Bot):
    def __init__(self):
        super().__init__()

    def decideBank(self, roundScore, game):
        return True

    def __str__(self):
        return f"CowardBot"
