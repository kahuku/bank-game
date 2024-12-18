import random
import csv
import argparse
from tqdm import tqdm
from collections import defaultdict

from Player import Player
from Game import Game
from bots.DumbBot import DumbBot
from bank_game import gameLoop

pcts = [(i / 100) for i in range(3, 33 + 1, 1)]
RANDOM_N_PLAYERS_MIN = 6
RANDOM_N_PLAYERS_MAX = 12

def simulateGame(num_players, num_rounds):
    players = [Player(f"Player {i}", DumbBot(bankThreshold=random.choice(pcts)), quiet=True) for i in range(1, num_players + 1)]

    game = Game(players, num_rounds, quiet=True)
    return gameLoop(game)

def writeSummaryData(records):
    def sortFunc(botType):
        return int(botType.split("(")[1][:-1])

    wins = defaultdict(int)
    data = defaultdict(list)

    for game in records:
        m = 0
        mb = None
        for name, botType, score in game:
            data[botType.__str__()].append(score)
            if score > m:
                m = score
                mb = botType
        wins[mb.__str__()] += 1

    for botType, scores in sorted(data.items(), key=lambda x: sortFunc(x[0])):
        print(f"Bot type: {botType}")
        print(f"- Average score: {sum(scores) / len(scores)}")
        print(f"- Median score: {sorted(scores)[len(scores) // 2]}")
        print(f"- Wins: {wins[botType]}")
        print(f"- Win rate: {wins[botType] / len(records) * 100:.2f}%")
        print()

def runSimulations(total_games, num_players, num_rounds, output_file):
    bot_scores = []

    # Run the game simulations with progress bar
    for game_index in tqdm(range(total_games), desc="Simulating games"):
        final_scores = simulateGame(num_players, num_rounds)
        bot_scores.append(final_scores)

    writeSummaryData(bot_scores)

    # Save results to a CSV file
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['GameIndex', 'PlayerName', 'BotType', 'Score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for game_index, scores in enumerate(bot_scores):
            for name, bot_type, score in scores:
                writer.writerow({
                    'GameIndex': game_index + 1,
                    'PlayerName': name,
                    'BotType': bot_type,
                    'Score': score
                })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Number of games to simulate", type=int, default=1_000)
    parser.add_argument("-n", help=f"Number of players per game, 0 for random {RANDOM_N_PLAYERS_MIN}-{RANDOM_N_PLAYERS_MAX}", type=int, default=6)
    parser.add_argument("-r", help="Number of rounds per game", type=int, default=10)
    parser.add_argument("-o", help="Output CSV file", type=str, default="bot_scores.csv")
    # parser.add_argument("-t", "--threads", help="Number of threads to use", type=int, default=1) # TODO: Implement threading
    args = parser.parse_args()

    if args.n == 0:
        args.n = random.randint(RANDOM_N_PLAYERS_MIN, RANDOM_N_PLAYERS_MAX)

    runSimulations(args.g, args.n, args.r, args.o)
