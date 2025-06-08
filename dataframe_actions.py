import time
import pandas as pd


# Chargement du dataset
dataset = pd.read_csv("dataset1.csv")
# Affiche toutes les lignes et colonnes
pd.set_option("display.max_rows", None)      # pour voir toutes les lignes
pd.set_option("display.max_columns", None)   # pour voir toutes les colonnes

# Affichage de la description du dataset
# dataset["price"] = (dataset["price"] * 100).astype(int)
# dataset["profit"] = (dataset["profit"] * 100).astype(int)

dataset["price"] = (dataset["price"])
dataset["profit"] = (dataset["profit"])

# print("Price ou Profit égal à 0")
# print(dataset[(dataset["price"] == 0) | (dataset["profit"] == 0)])
# dataset = dataset[(dataset["price"] != 0) & (dataset["profit"] != 0)]
dataset = dataset[(dataset["price"] > 0) & (dataset["profit"] > 0)]
print(dataset.describe())
print(dataset)
