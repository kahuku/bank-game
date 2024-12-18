import random

class Game:
    def __init__(self, players, rounds, quiet=False):
        self.quiet = quiet

        self.currentRound = 1

        self.players = players
        self.rounds = rounds
        self.playerTurn = 0
        self.unbankedPlayers = set(range(len(players)))

    def printScores(self): 
        if not self.quiet:
            print("SCOREBOARD")
            for player in self.players:
                print(player)
            print()

    def calculateRoundScore(self, count, dupes, roundScore, rollCount):
        if rollCount < 3:
            return False, roundScore + 70 if count == 7 else count
        if count == 7: return True, 0
        return False, roundScore * 2 if dupes else roundScore
        
    def playRound(self):
        for player in self.players:
            player.banked = False
        self.unbankedPlayers = set(range(len(self.players)))

        if not self.quiet:
            print("=" * 20)
            print(f"Round {self.currentRound}")
            print("=" * 20)
            self.printScores()

        rollCount = 0
        roundScore = 0
        while True:
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            dupes = d1 == d2
            count = d1 + d2
            if not self.quiet:
                print(f"{self.players[self.playerTurn].name}'s turn")
                print(f"Rolled {count} {'(doubles)' if dupes else ''}")
                print("Current score:", roundScore)
            rollCount += 1 

            rolledEnd, roundScore = self.calculateRoundScore(count, dupes, roundScore, rollCount)

            self.updatePlayerTurn()
            if rolledEnd:
                for playerIndex in self.unbankedPlayers:
                    self.players[playerIndex].roundScores.append(0)
                self.currentRound += 1
                return

            if rollCount >= 3:
                self.bankOpportunity(roundScore)

            if len(self.unbankedPlayers) == 0:
                if not self.quiet:
                    print(f"Round {self.currentRound} over\n")
                self.currentRound += 1
                return

    def checkOver(self):
        return self.currentRound > self.rounds

    def updatePlayerTurn(self):
        self.playerTurn = (self.playerTurn + 1) % len(self.players)
        if len(self.unbankedPlayers) == 0: return
        while self.players[self.playerTurn].banked:
            self.playerTurn = (self.playerTurn + 1) % len(self.players)

    def bankOpportunity(self, roundScore):
        toRemove = set()
        for playerIndex in self.unbankedPlayers:
            if self.players[playerIndex].decideBank(roundScore, self):
                toRemove.add(playerIndex)
        if not self.quiet:
            print()
        self.unbankedPlayers -= toRemove

    def end(self):
        self.printScores()
        winner = max(self.players, key=lambda x: x.score)
        if not self.quiet:
            print(f"{winner.name} wins with {winner.score} points!")
