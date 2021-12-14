import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("D:/games.csv")

df.drop(["id","created_at","last_move_at","increment_code"],axis = 1, inplace = True)
#remove data
print(df.describe())
print("\n")

rated = df["rated"].value_counts()
print(rated)
print("\n")

offical_match_mean = df["rated"].mean()
print(f"공식 경기일 확률: {offical_match_mean}")
print("\n")

offical_match = df.loc[df["rated"] == 1]

turns = df[["rated","turns"]].groupby("rated").mean()
print(turns)
print("\n")

turns_hist = df[['turns']].plot(kind = 'hist',rwidth = 0.8)
plt.show()

victory = df["victory_status"].value_counts()
print(victory)
print("\n")

winner = df["winner"].value_counts()
print(winner)
print("\n")

opening_eco = df["opening_eco"].value_counts().head(10)
print(opening_eco)
print("\n")

opening_ply = df["opening_ply"].value_counts().head(10)
print(opening_ply)
print("\n")