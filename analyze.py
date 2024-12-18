import pandas as pd
import matplotlib.pyplot as plt


# current analysis setup assumes one bot of each type per game


# Load the data
df = pd.read_csv("data/bot_scores.csv")

# Add a column to indicate the winning bot in each game
df['is_winner'] = df.groupby('GameIndex')['Score'].transform(max) == df['Score']

# Calculate win rate per bot type
# THIS IS WRONG -- DIVIDE BY NUMBER OF GAMES THAT BOT PARTICIPATED IN
# win_rates = df[df['is_winner']].groupby('BotType')['is_winner'].count() / df['GameIndex'].nunique()


# Calculate the number of games each bot type participated in
games_played = df.groupby('BotType')['GameIndex'].nunique()

# Calculate the number of games each bot type won
wins = df[df['is_winner']].groupby('BotType')['is_winner'].count()

# Calculate the win rate for each bot type
win_rates = wins / games_played


# Calculate average score per bot type
avg_scores = df.groupby('BotType')['Score'].mean()

# Calculate score variance per bot type
score_variance = df.groupby('BotType')['Score'].var()

# Calculate median score per bot type
median_scores = df.groupby('BotType')['Score'].median()

# Assemble plot
plt.figure(figsize=(12, 6))

plt.subplot(1, 4, 1)
win_rates.plot(kind='bar', title='Win Rate by Bot Type')
plt.ylabel('Win Rate')

plt.subplot(1, 4, 2)
avg_scores.plot(kind='bar', title='Average Score by Bot Type')
plt.ylabel('Average Score')

plt.subplot(1, 4, 3)
score_variance.plot(kind='bar', title='Score Variance by Bot Type')
plt.ylabel('Score Variance')

plt.subplot(1, 4, 4)
median_scores.plot(kind='bar', title='Median Score by Bot Type')
plt.ylabel('Median Score')

plt.tight_layout()
plt.show()