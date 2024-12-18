import random
import csv
import argparse
import time
from tqdm import tqdm
from collections import defaultdict
import concurrent.futures

from Player import Player
from Game import Game
from bots.DumbBot import DumbBot
from bots.MedianBot import MedianBot
from bots.CowardBot import CowardBot
from bots.ExpectedBot import ExpectedBot
from bank_game import gameLoop

RANDOM_N_PLAYERS_MIN = 6
RANDOM_N_PLAYERS_MAX = 12

pcts = [.2, .3, .15, .25]
pcts2 = [.25, .5, .75]

def simulateGame(num_players, num_rounds):
    players = [Player("DumbBot", DumbBot(bankThreshold=random.choice(pcts)), quiet=True) for _ in range(num_players - 3)]
    players.extend([Player("MedianBot", MedianBot(bankThreshold=random.choice(pcts), playerThreshold=random.choice(pcts2)), quiet=True) for _ in range(2)])
    players.append(Player("ExpectedBot", ExpectedBot(), quiet=True))

    game = Game(players, num_rounds, quiet=True)
    return gameLoop(game)

def writeSummaryData(records):
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

    def sortFunc(botType):
        return int(botType.split("(")[1][:-1])

    for botType, scores in sorted(data.items(), key=lambda x: sortFunc(x[0])):
        print(f"Bot type: {botType}")
        print(f"- Average score: {sum(scores) / len(scores)}")
        print(f"- Median score: {sorted(scores)[len(scores) // 2]}")
        print(f"- Wins: {wins[botType]}")
        print(f"- Win rate: {wins[botType] / len(records) * 100:.2f}%")
        print()

def simulateGameThreaded(num_simulations, num_players, num_rounds, i):
    results = []
    for _ in tqdm(range(num_simulations), desc=f"Simulating games -- Process #{i}", position=i):
    # for _ in range(num_simulations):
        results.append(simulateGame(num_players, num_rounds))
    return results

def runSimulations(total_games, num_players, num_rounds, output_file, threads):
    sims_per_thread = total_games // threads
    allResults = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
        # Distribute simulations across threads
        futures = [
            executor.submit(simulateGameThreaded, sims_per_thread, num_players, num_rounds, i + 1)
            for i in range(threads)
        ]
        
        # Gather results from each thread
        for future in concurrent.futures.as_completed(futures):
            allResults.extend(future.result())

    # writeSummaryData(allResults)

    logTime = time.time()

    # Save results to a CSV file
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Game', 'PlayerName', 'BotType', 'Place', 'Score']
        fieldnames.extend([f"Round {i + 1} Score" for i in range(num_rounds)])
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for game_index, scores in enumerate(allResults):
            scores.sort(key=lambda x: x[2], reverse=True)
            k = 1
            for name, bot_type, score, roundScores in scores:
                row = {
                    'Game': game_index + 1,
                    'PlayerName': name,
                    'BotType': bot_type.__str__(),
                    'Place': k,
                    'Score': score
                }
                row.update({f"Round {j + 1} Score": s for j, s in enumerate(roundScores)})
                writer.writerow(row)
                k += 1
    print(f"Log time: {time.time() - logTime:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Number of games to simulate", type=int, default=1_000)
    parser.add_argument("-n", help=f"Number of players per game, 0 for random {RANDOM_N_PLAYERS_MIN}-{RANDOM_N_PLAYERS_MAX}", type=int, default=6)
    parser.add_argument("-r", help="Number of rounds per game", type=int, default=10)
    parser.add_argument("-o", help="Output CSV file", type=str, default="bot_scores.csv")
    parser.add_argument("-t", "--threads", help="Number of threads (actually processes) to use", type=int, default=1)
    args = parser.parse_args()

    if args.n == 0:
        args.n = random.randint(RANDOM_N_PLAYERS_MIN, RANDOM_N_PLAYERS_MAX)

    startTime = time.time()

    runSimulations(args.g, args.n, args.r, args.o, args.threads)

    print(f"Time taken: {time.time() - startTime:.2f} seconds")