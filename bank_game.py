import argparse
import random

from Player import Player
from Game import Game
from bots.DumbBot import DumbBot

bots = [DumbBot()]

def gameLoop(game):
    while not game.checkOver():
        game.playRound()

    if not game.quiet:
        print("Game over!")
        game.end()

    endGameOutput = []
    for player in game.players:
        line = [player.name, player.brain, player.score, player.roundScores]
        endGameOutput.append(line)
    return endGameOutput

def initPlayers(n, quiet):
    players = []
    for i in range(n):
        name = input(f"Enter name for Player {i + 1}: ")
        bot = input(f"Is {name} a bot? (y/n): ")
        if bot == "y":
            botClassStr = input(f"Enter bot class for {name} (Dumb): ")
            if botClassStr == "Dumb":
                players.append(Player(name, DumbBot(), quiet=quiet))
            else:
                print("Invalid bot class. Defaulting to DumbBot.")
                players.append(Player(name, DumbBot(), quiet=quiet))
        else:
            players.append(Player(name, None, quiet=quiet))
    return players

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="Number of players", type=int, default=6)
    parser.add_argument("-r", help="Number of rounds", type=int, default=10)
    parser.add_argument("--autoName", help="Automatically name players", type=bool, default=False)
    parser.add_argument("--autoBot", help="Automatically name players and assign all as a random choice of bots", type=bool, default=False)
    parser.add_argument("-q", "--quiet", help="Quiet mode", type=bool, default=False)
    args = parser.parse_args()

    if args.autoBot:
        players = [Player(f"Player {i}", random.choice(bots), quiet=True) for i in range(1, args.n + 1)]
    elif args.autoName:
        players = [Player(f"Player {i}", None, quiet=True) for i in range(1, args.n + 1)]
    else:
        players = initPlayers(args.n, args.quiet)
    
    game = Game(players, args.r, args.quiet)

    if not args.quiet:
        print("Bank Game starting...\n")
    gameLoop(game)
